import os
from typing import Any, Dict, Optional

from openai import OpenAI


def translate_platform_output(text: str, target_locale: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Translate the given platform model output into the target locale while preserving meaning, formatting, and any technical tokens. Return only the translated text.",
            },
            {
                "role": "user",
                "content": f"Target locale: {target_locale}\n\nPlatform output:\n{text}",
            },
        ],
    )
    return response.output_text


def localize_platform_output(payload: Dict[str, Any], target_locale: str) -> Dict[str, Any]:
    localized = dict(payload)
    for key in ("output", "message", "text", "content"):
        value = localized.get(key)
        if isinstance(value, str):
            localized[key] = translate_platform_output(value, target_locale)
    return localized
