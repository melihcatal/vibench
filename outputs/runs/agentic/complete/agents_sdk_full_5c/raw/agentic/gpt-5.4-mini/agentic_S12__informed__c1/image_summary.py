from __future__ import annotations

from openai import OpenAI

from vision_models import LabelResult, SafetyResult, TextResult

MODEL_ID = "gpt-4o-mini"


def summarize_visual_analysis(labels: list[LabelResult], texts: list[TextResult], safety: SafetyResult | None = None) -> str:
    client = OpenAI()
    payload = {
        "labels": [label.__dict__ for label in labels],
        "texts": [text.__dict__ for text in texts],
        "safety": None if safety is None else safety.__dict__,
    }
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Summarize image analysis results briefly."},
            {"role": "user", "content": str(payload)},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
