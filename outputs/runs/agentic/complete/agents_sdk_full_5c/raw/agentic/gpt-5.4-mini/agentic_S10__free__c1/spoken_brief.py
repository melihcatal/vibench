from __future__ import annotations

from model_client import get_model_name, get_openai_client

PROVIDER = "openai"
MODEL_FAMILY = "gpt-4o-mini"


def spoken_brief(text: str, model: str | None = None) -> str:
    client = get_openai_client()
    response = client.responses.create(
        model=get_model_name(model),
        input=[
            {
                "role": "system",
                "content": "Turn the text into a short spoken brief suitable for text-to-speech. Keep it natural and concise.",
            },
            {"role": "user", "content": text},
        ],
    )
    return response.output_text
