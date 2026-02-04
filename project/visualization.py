"""Visualization utilities using matplotlib/seaborn."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")


def plot_distribution(df: pd.DataFrame, column: str, title: str) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(6, 4))
    counts = df[column].value_counts(dropna=False)
    sns.barplot(x=counts.index, y=counts.values, ax=ax, palette="muted")
    ax.set_title(title)
    ax.set_ylabel("Count")
    ax.set_xlabel(column.capitalize())
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    return fig


def plot_grouped_distribution(
    df: pd.DataFrame, group_col: str, target_col: str, title: str
) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(8, 4))
    grouped = df.groupby(group_col)[target_col].value_counts().unstack(fill_value=0)
    grouped.plot(kind="bar", stacked=True, ax=ax, colormap="tab20")
    ax.set_title(title)
    ax.set_ylabel("Count")
    ax.set_xlabel(group_col)
    ax.legend(title=target_col, bbox_to_anchor=(1.02, 1), loc="upper left")
    fig.tight_layout()
    return fig


def plot_negative_deep_dive(df: pd.DataFrame) -> plt.Figure:
    negative_df = df[df["sentiment"] == "Negative"]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    sns.countplot(x="intent", data=negative_df, ax=axes[0], palette="Reds")
    axes[0].set_title("Negative Feedback by Intent")
    axes[0].tick_params(axis="x", rotation=30)
    sns.countplot(x="emotion", data=negative_df, ax=axes[1], palette="Reds")
    axes[1].set_title("Negative Feedback by Emotion")
    axes[1].tick_params(axis="x", rotation=30)
    fig.tight_layout()
    return fig


def plot_score_vs_sentiment(df: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(x="sentiment", y="score", data=df, ax=ax, palette="pastel")
    ax.set_title("Score vs Sentiment")
    fig.tight_layout()
    return fig
