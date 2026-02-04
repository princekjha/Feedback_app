"""Utility helpers for feedback analytics."""

from __future__ import annotations

import re
from typing import Optional

import pandas as pd

COLUMN_REGEX = re.compile(r"(comment|feedback|suggestion|review|text|desc|note)", re.I)


def safe_text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return ""


def detect_feedback_column(df: pd.DataFrame) -> Optional[str]:
    best_column = None
    best_score = -1.0
    for column in df.columns:
        if not pd.api.types.is_string_dtype(df[column]):
            continue
        series = df[column].dropna().astype(str)
        if series.empty:
            continue
        avg_length = series.str.len().mean()
        score = 0.0
        if COLUMN_REGEX.search(column):
            score += 2.0
        if avg_length > 20:
            score += 1.0
        score += avg_length / 100.0
        if score > best_score:
            best_score = score
            best_column = column
    return best_column


def truncate_text(text: str, max_len: int = 60) -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - 3].rstrip() + "..."
