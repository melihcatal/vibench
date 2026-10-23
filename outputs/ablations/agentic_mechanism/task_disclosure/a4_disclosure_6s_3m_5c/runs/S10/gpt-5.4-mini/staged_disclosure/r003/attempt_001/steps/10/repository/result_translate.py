import os
from typing import Optional

from openai import OpenAI


DEFAULT_TRANSLATION_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")


def _client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL"))


def translate_result(text: str, target_language: str, source_language: Optional[str] = None, model: Optional[str] = None) -> str:
    source_note = f" from {source_language}" if source_language else ""
    prompt = f"Translate the following generated model output{source_note} into {target_language}. Preserve meaning, formatting, code blocks, and lists. Return only the translation.\n\n{text}"
    response = _client().responses.create(
        model=model or DEFAULT_TRANSLATION_MODEL,
        input=[
            {"role": "system", "content": "You are a precise translation engine."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
        max_output_tokens=2048,
    )
    return getattr(response, "output_text", "") or ""
