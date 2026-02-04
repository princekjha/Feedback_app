"""Analysis engine for feedback analytics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from prompts import SUMMARY_PROMPT
from utils import safe_text, truncate_text

NEGATIVE_CONTEXT_WORDS = [
    "unpleasant",
    "dissatisfied",
    "no proper",
    "lack of",
    "not managed",
    "poor",
    "delay",
    "issue",
    "problem",
    "failed",
    "only",
    "despite",
    "did not",
    "no management",
    "low turnout",
    "not attended",
]

INTENT_KEYWORDS = {
    "Complaint": [
        "issue",
        "problem",
        "unpleasant",
        "dissatisfied",
        "no proper",
        "lack of",
        "not managed",
        "poor",
        "delay",
        "failed",
        "only",
        "despite",
        "did not",
        "no management",
    ],
    "Suggestion": [
        "should",
        "could",
        "recommend",
        "improve",
        "need to",
        "ensure",
    ],
    "Appreciation": [
        "good",
        "great",
        "helpful",
        "excellent",
        "thanks",
        "support",
    ],
    "Query": [
        "how",
        "why",
        "what",
        "when",
        "?",
    ],
}

INTENT_PRIORITY = [
    "Complaint",
    "Suggestion",
    "Appreciation",
    "Query",
    "General Feedback",
]


@dataclass
class AnalysisConfig:
    mode: str = "quick"
    model: str = "llama3.2"
    temperature: float = 0.3
    max_tokens: int = 50
    ollama_url: str = "http://localhost:11434/api/generate"


def empty_result() -> Dict[str, object]:
    return {
        "sentiment": "N/A",
        "score": 0.0,
        "emotion": "None",
        "intent": "N/A",
        "summary": "Empty feedback",
    }


def _apply_negative_penalties(text: str, compound: float) -> float:
    lowered = text.lower()
    penalty = 0.0
    for phrase in NEGATIVE_CONTEXT_WORDS:
        occurrences = lowered.count(phrase)
        if occurrences:
            penalty += 0.15 * occurrences
    return compound - penalty


def analyze_sentiment(text: str, analyzer: SentimentIntensityAnalyzer) -> Dict[str, object]:
    scores = analyzer.polarity_scores(text)
    compound = _apply_negative_penalties(text, scores["compound"])
    compound = max(-1.0, min(1.0, compound))
    if compound >= 0.30:
        sentiment = "Positive"
    elif compound <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    return {"sentiment": sentiment, "score": round(compound, 2)}


def classify_intent(text: str) -> str:
    lowered = text.lower()
    for intent in INTENT_PRIORITY:
        if intent == "General Feedback":
            return "General Feedback"
        keywords = INTENT_KEYWORDS.get(intent, [])
        if any(keyword in lowered for keyword in keywords):
            return intent
    return "General Feedback"


def infer_emotion(sentiment: str, intent: str, is_empty: bool) -> str:
    if is_empty:
        return "None"
    if intent == "Complaint":
        return "Frustrated"
    if sentiment == "Negative":
        return "Dissatisfied"
    if sentiment == "Positive":
        return "Satisfied"
    return "Neutral"


def generate_summary(text: str, config: AnalysisConfig) -> str:
    if len(text) <= 30:
        return text
    if config.mode != "ai":
        return truncate_text(text, max_len=60)
    payload = {
        "model": config.model,
        "prompt": f"{SUMMARY_PROMPT}\n\n{text}",
        "temperature": config.temperature,
        "max_tokens": config.max_tokens,
        "stream": False,
    }
    try:
        response = requests.post(config.ollama_url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        summary = safe_text(data.get("response", ""))
    except requests.RequestException:
        return truncate_text(text, max_len=60)
    if len(summary) <= 10 or summary.lower() == text.lower():
        return truncate_text(text, max_len=60)
    return summary


def analyze_text(text: object, analyzer: SentimentIntensityAnalyzer, config: AnalysisConfig) -> Dict[str, object]:
    cleaned = safe_text(text)
    if len(cleaned) < 3:
        return empty_result()
    sentiment_result = analyze_sentiment(cleaned, analyzer)
    intent = classify_intent(cleaned)
    emotion = infer_emotion(sentiment_result["sentiment"], intent, False)
    summary = generate_summary(cleaned, config)
    return {
        "sentiment": sentiment_result["sentiment"],
        "score": sentiment_result["score"],
        "emotion": emotion,
        "intent": intent,
        "summary": summary,
    }


def analyze_series(series, config: AnalysisConfig) -> List[Dict[str, object]]:
    analyzer = SentimentIntensityAnalyzer()
    return [analyze_text(value, analyzer, config) for value in series]
