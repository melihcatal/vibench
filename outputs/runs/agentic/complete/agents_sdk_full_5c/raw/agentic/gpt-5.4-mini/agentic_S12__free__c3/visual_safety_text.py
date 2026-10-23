from __future__ import annotations

from openai import OpenAI

MODEL_ID = "gpt-4o-mini"


def visual_safety_text(labels_text: str) -> str:
    client = OpenAI()
    response = client.responses.create(
        model=MODEL_ID,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": f"Review the following image labels for unsafe or sensitive text and respond with a short risk note: {labels_text}"},
                ],
            }
        ],
    )
    return (getattr(response, "output_text", "") or "").strip()
