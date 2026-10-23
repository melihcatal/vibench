from __future__ import annotations

from model_client import get_model_name, get_openai_client

PROVIDER = "openai"
MODEL_FAMILY = "gpt-4o"


def summarize_text(text: str, model: str | None = None) -> str:
    client = get_openai_client()
    response = client.responses.create(
        model=get_model_name(model),
        input=[
            {
                "role": "system",
                "content": "You are a concise summarizer. Summarize the text in a clear, factual paragraph.",
            },
            {"role": "user", "content": text},
        ],
    )
    return response.output_text
