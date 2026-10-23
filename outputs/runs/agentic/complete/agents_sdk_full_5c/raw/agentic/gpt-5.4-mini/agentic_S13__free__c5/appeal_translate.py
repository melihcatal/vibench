from __future__ import annotations

from safety_client import get_client, get_config


def appeal_translate(text: str, target_language: str = "en") -> str:
    config = get_config()
    client = get_client(config.api_key)
    response = client.responses.create(
        model=config.translation_model,
        input=f"Translate the following appeal text into {target_language} while preserving meaning:\n{text}",
    )
    return response.output_text
