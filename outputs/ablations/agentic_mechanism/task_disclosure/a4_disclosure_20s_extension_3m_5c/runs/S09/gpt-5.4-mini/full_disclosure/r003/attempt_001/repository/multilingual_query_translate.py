import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


DEFAULT_TRANSLATION_MODEL = os.environ.get("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini")


@dataclass(frozen=True)
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: Optional[str] = None
    target_language: str = "en"


def get_translation_client(api_key: Optional[str] = None) -> OpenAI:
    return OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))


def translate_query(query: str, target_language: str = "en", model: Optional[str] = None, api_key: Optional[str] = None) -> TranslationResult:
    client = get_translation_client(api_key=api_key)
    model_name = model or DEFAULT_TRANSLATION_MODEL
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "Translate the user's search query into the target language. Return only the translated text."},
            {"role": "user", "content": f"Target language: {target_language}\nQuery: {query}"},
        ],
        temperature=0,
    )
    translated_text = response.choices[0].message.content or ""
    return TranslationResult(source_text=query, translated_text=translated_text.strip(), target_language=target_language)
