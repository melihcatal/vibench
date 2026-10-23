import os
from typing import Any, Dict

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def translate_platform_output(output: str, locale: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "system",
                "content": "Translate platform model output into the requested locale. Preserve meaning, formatting, code blocks, identifiers, product names, and markup. Return only the translated text.",
            },
            {
                "role": "user",
                "content": f"Locale: {locale}\n\nOutput:\n{output}",
            },
        ],
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()

    try:
        return data["output"][0]["content"][0]["text"]
    except (KeyError, IndexError, TypeError):
        raise RuntimeError("Unexpected response format from OpenAI Responses API")
