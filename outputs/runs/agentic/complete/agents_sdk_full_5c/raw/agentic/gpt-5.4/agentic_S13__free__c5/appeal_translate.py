from __future__ import annotations

from safety_client import OPENAI_TRANSLATION_MODEL, get_openai_client


def translate_appeal_text(appeal_text: str, target_language: str = "en") -> str:
    client = get_openai_client()
    response = client.responses.create(
        model=OPENAI_TRANSLATION_MODEL,
        input=[
            {
                "role": "system",
                "content": f"Translate user moderation appeals into {target_language} while preserving tone and factual details.",
            },
            {"role": "user", "content": appeal_text},
        ],
    )
    return response.output_text
