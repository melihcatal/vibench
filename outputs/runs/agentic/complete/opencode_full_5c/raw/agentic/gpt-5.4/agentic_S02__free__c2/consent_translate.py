from __future__ import annotations

import os

from openai import OpenAI


def translate_consent_copy(text: str, target_language: str) -> dict[str, str]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Translate identity-provider consent copy into {target_language} while preserving meaning and compliance tone.",
                    }
                ],
            },
            {"role": "user", "content": [{"type": "input_text", "text": text}]},
        ],
    )
    return {
        "provider": "openai",
        "model": "gpt-4.1-mini",
        "target_language": target_language,
        "translation": response.output_text,
    }
