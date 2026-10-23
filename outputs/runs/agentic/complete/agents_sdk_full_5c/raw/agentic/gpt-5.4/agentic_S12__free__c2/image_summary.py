from __future__ import annotations

from typing import Iterable, List, Mapping

from openai import OpenAI


OPENAI_MODEL = "gpt-4.1-mini"


def image_summary(labels: Iterable[str], description: str, detected_text: Iterable[str], safety_flags: Iterable[str], api_key: str | None = None) -> str:
    client = OpenAI(api_key=api_key)
    prompt = {
        "labels": list(labels),
        "description": description,
        "detected_text": list(detected_text),
        "safety_flags": list(safety_flags),
    }
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=f"Summarize this visual analysis in 2 concise sentences: {prompt}",
    )
    return (response.output_text or "").strip()
