from __future__ import annotations

from translation_client import get_client


def quality_summary(text: str):
    client = get_client()
    return client.summarize_quality(text)
