import os

from model_client import get_client, get_model_name, normalize_text


def summarize_text(text: str) -> str:
    client = get_client()
    response = client.responses.create(
        model=get_model_name(),
        input=[
            {
                "role": "system",
                "content": "Summarize long text clearly and concisely.",
            },
            {"role": "user", "content": normalize_text(text)},
        ],
    )
    return response.output_text
