import os
from typing import Optional, Dict, Any, List

import openai
from openai import OpenAI

from security_models import ComplianceTranslation

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
TRANSLATION_MODEL = os.environ.get("TRANSLATION_MODEL", "gpt-4o-mini")

SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "ja": "Japanese",
    "zh": "Chinese (Simplified)",
    "pt": "Portuguese",
    "it": "Italian",
    "ko": "Korean",
    "ru": "Russian",
    "ar": "Arabic",
    "hi": "Hindi",
}

COMPLIANCE_TRANSLATION_PROMPT = """You are a compliance and encryption specialist translator. Translate the following encryption or compliance note from {source_lang} to {target_lang}.

Preserve all technical terminology accurately. If a term has a widely recognized equivalent in the target language, use it. Otherwise, keep the original term and add a brief explanation in parentheses if needed.

Maintain the formal, professional tone appropriate for compliance documentation.

Original text:
---
{text}
---

Provide only the translated text, with no additional commentary."""


def translate_compliance_note(
    text: str,
    source_language: str = "en",
    target_language: str = "es",
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    key_id: Optional[str] = None,
) -> Dict[str, Any]:
    target_model = model or TRANSLATION_MODEL
    target_api_key = api_key or OPENAI_API_KEY
    target_base_url = base_url or OPENAI_BASE_URL

    if not target_api_key:
        raise ValueError(
            "OpenAI API key is required. Set OPENAI_API_KEY environment variable."
        )

    if source_language not in SUPPORTED_LANGUAGES:
        raise ValueError(
            f"Unsupported source language: {source_language}. Supported: {list(SUPPORTED_LANGUAGES.keys())}"
        )
    if target_language not in SUPPORTED_LANGUAGES:
        raise ValueError(
            f"Unsupported target language: {target_language}. Supported: {list(SUPPORTED_LANGUAGES.keys())}"
        )

    source_lang_name = SUPPORTED_LANGUAGES[source_language]
    target_lang_name = SUPPORTED_LANGUAGES[target_language]

    prompt = COMPLIANCE_TRANSLATION_PROMPT.format(
        source_lang=source_lang_name,
        target_lang=target_lang_name,
        text=text,
    )

    client = OpenAI(api_key=target_api_key, base_url=target_base_url)

    response = client.chat.completions.create(
        model=target_model,
        messages=[
            {
                "role": "system",
                "content": "You are a professional compliance and encryption specialist translator. Translate technical compliance documents accurately while preserving terminology.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=2048,
    )

    translated_text = response.choices[0].message.content.strip()

    translation = ComplianceTranslation(
        original_text=text,
        translated_text=translated_text,
        source_language=source_language,
        target_language=target_language,
        model=target_model,
        key_id=key_id,
    )

    return {
        "original_text": translation.original_text,
        "translated_text": translation.translated_text,
        "source_language": translation.source_language,
        "source_language_name": source_lang_name,
        "target_language": translation.target_language,
        "target_language_name": target_lang_name,
        "model": translation.model,
        "key_id": translation.key_id,
    }


def translate_compliance_notes_batch(
    texts: List[str],
    source_language: str = "en",
    target_language: str = "es",
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    key_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    results = []
    for text in texts:
        try:
            result = translate_compliance_note(
                text=text,
                source_language=source_language,
                target_language=target_language,
                model=model,
                api_key=api_key,
                base_url=base_url,
                key_id=key_id,
            )
            results.append(result)
        except Exception as exc:
            results.append(
                {
                    "original_text": text[:200],
                    "error": str(exc),
                    "source_language": source_language,
                    "target_language": target_language,
                    "model": model or TRANSLATION_MODEL,
                }
            )
    return results
