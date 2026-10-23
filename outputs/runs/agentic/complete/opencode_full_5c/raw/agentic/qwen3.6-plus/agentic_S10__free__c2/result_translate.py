from __future__ import annotations

from typing import Optional

from model_client import call_llm
from model_models import LLMRequest, TranslationResponse, normalize_prompt

TRANSLATOR_MODEL = "gpt-4o"
TRANSLATOR_SYSTEM_TEMPLATE = (
    "You are a professional translator. Translate the provided text from {source_lang} "
    "to {target_lang}. Preserve the original meaning, tone, and formatting. "
    "Return only the translated text without explanations."
)

LANGUAGE_MAP = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "pt": "Portuguese",
    "ru": "Russian",
    "ar": "Arabic",
    "hi": "Hindi",
    "it": "Italian",
}


def _resolve_language_name(code: str) -> str:
    return LANGUAGE_MAP.get(code.lower(), code)


def translate_result(
    text: str,
    target_language: str = "en",
    source_language: str = "auto",
    temperature: float = 0.3,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> TranslationResponse:
    normalized = normalize_prompt(text)
    target_name = _resolve_language_name(target_language)
    source_name = (
        _resolve_language_name(source_language)
        if source_language != "auto"
        else "the detected source language"
    )
    system_prompt = TRANSLATOR_SYSTEM_TEMPLATE.format(
        source_lang=source_name, target_lang=target_name
    )
    prompt = f"Translate the following text:\n\n{normalized}"
    request = LLMRequest(
        model=model or TRANSLATOR_MODEL,
        prompt=prompt,
        system_prompt=system_prompt,
        temperature=temperature,
        max_tokens=4096,
    )
    response = call_llm(request, api_key=api_key, base_url=base_url)
    return TranslationResponse(
        translated_text=response.text,
        source_language=source_language,
        target_language=target_language,
        model_used=response.model_used,
        raw=response.raw,
    )


def translate_batch(
    texts: list[str],
    target_language: str = "en",
    source_language: str = "auto",
    temperature: float = 0.3,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> list[TranslationResponse]:
    results = []
    for text in texts:
        result = translate_result(
            text=text,
            target_language=target_language,
            source_language=source_language,
            temperature=temperature,
            model=model,
            api_key=api_key,
            base_url=base_url,
        )
        results.append(result)
    return results


if __name__ == "__main__":
    import os

    response = translate_result(
        text="Bonjour le monde, comment allez-vous aujourd'hui?",
        target_language="en",
        source_language="fr",
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    print(response.translated_text)
