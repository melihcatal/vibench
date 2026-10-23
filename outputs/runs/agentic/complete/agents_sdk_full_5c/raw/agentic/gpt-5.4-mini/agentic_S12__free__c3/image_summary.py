from __future__ import annotations

from typing import Iterable, Mapping

from openai import OpenAI

MODEL_ID = "gpt-4o-mini"


def image_summary(labels: Iterable[Mapping[str, object]], ocr_text: str, description: str) -> str:
    client = OpenAI()
    prompt = {
        "labels": list(labels),
        "ocr_text": ocr_text,
        "description": description,
    }
    response = client.responses.create(
        model=MODEL_ID,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": f"Write a concise summary of this image analysis: {prompt}"},
                ],
            }
        ],
    )
    return (getattr(response, "output_text", "") or "").strip()
