from __future__ import annotations

from safety_client import get_openai_client


def appeal_translate(text: str, target_language: str = "en") -> str:
    client = get_openai_client()
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": f"Translate user moderation appeals into {target_language} while preserving tone and factual meaning.",
            },
            {"role": "user", "content": text},
        ],
    )
    return response.output_text
