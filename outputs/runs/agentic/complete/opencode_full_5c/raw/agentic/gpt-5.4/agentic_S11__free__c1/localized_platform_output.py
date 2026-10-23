from __future__ import annotations

from model_client import get_openai_client


def localized_platform_output(text: str, target_locale: str) -> object:
    client = get_openai_client()
    return client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": f"Translate the user content into locale {target_locale}.",
            },
            {"role": "user", "content": text},
        ],
        temperature=0,
    )
