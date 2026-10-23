from __future__ import annotations

from model_client import get_model_name, get_openai_client

PROVIDER = "openai"
MODEL_FAMILY = "gpt-4o-mini"


def result_translate(text: str, target_language: str, model: str | None = None) -> str:
    client = get_openai_client()
    response = client.responses.create(
        model=get_model_name(model),
        input=[
            {
                "role": "system",
                "content": f"Translate the text into {target_language} while preserving meaning, tone, and formatting.",
            },
            {"role": "user", "content": text},
        ],
    )
    return response.output_text
