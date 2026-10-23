from __future__ import annotations

import os

import deepl



def translate_query_for_multilingual_search(
    query: str,
    target_lang: str,
    source_lang: str | None = None,
    glossary_id: str | None = None,
) -> dict[str, str]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise EnvironmentError("DEEPL_AUTH_KEY is required")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        query,
        source_lang=source_lang,
        target_lang=target_lang,
        glossary=glossary_id,
        preserve_formatting=True,
    )
    detected_source = source_lang or getattr(result, "detected_source_lang", "")
    return {
        "provider": "DeepL",
        "source_language": detected_source,
        "target_language": target_lang,
        "translated_text": result.text,
    }
