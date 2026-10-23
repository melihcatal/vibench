import os
from typing import Optional

from openai import OpenAI


DEFAULT_TRANSLATION_MODEL = "openai/gpt-5.4-mini"


def translate_result(text: str, target_language: str, model: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), base_url=os.environ.get("OPENAI_BASE_URL"))
    model_id = model or os.environ.get("OPENAI_MODEL", DEFAULT_TRANSLATION_MODEL)
    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {
                "role": "system",
                "content": "Translate the given model output into the target language while preserving meaning, tone, formatting, and any code or identifiers exactly unless translation is required.",
            },
            {
                "role": "user",
                "content": f"Target language: {target_language}\n\nText:\n{text}",
            },
        ],
        temperature=0,
    )
    return response.choices[0].message.content or ""
