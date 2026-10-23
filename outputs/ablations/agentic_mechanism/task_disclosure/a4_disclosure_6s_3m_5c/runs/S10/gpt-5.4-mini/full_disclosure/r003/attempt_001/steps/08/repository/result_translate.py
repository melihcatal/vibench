import os
from typing import Optional

from openai import OpenAI


DEFAULT_TRANSLATION_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", os.getenv("OPENAI_MODEL", "gpt-5.4-mini"))


def result_translate(text: str, target_language: str, model: Optional[str] = None, api_key: Optional[str] = None) -> str:
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model=model or DEFAULT_TRANSLATION_MODEL,
        input=[
            {
                "role": "system",
                "content": f"Translate the provided model output into {target_language}. Preserve meaning, tone, formatting, and any code or identifiers. Return only the translation.",
            },
            {"role": "user", "content": text},
        ],
        temperature=0,
    )
    return response.output_text
