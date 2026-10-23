import os
import deepl
from typing import List


DEEPL_AUTH_KEY_ENV = "DEEPL_AUTH_KEY"
DEEPL_DEFAULT_SOURCE_LANG = "EN"


def get_deepl_client() -> deepl.Translator:
    auth_key = os.environ.get(DEEPL_AUTH_KEY_ENV)
    if not auth_key:
        raise ValueError(
            f"DeepL auth key not found. Set the {DEEPL_AUTH_KEY_ENV} environment variable."
        )
    return deepl.Translator(auth_key)


def translate_script(
    text: str,
    target_lang: str,
    source_lang: str = None,
    preserve_formatting: bool = True,
) -> str:
    translator = get_deepl_client()

    result = translator.translate_text(
        text,
        source_lang=source_lang if source_lang else None,
        target_lang=target_lang.upper(),
        preserve_formatting=preserve_formatting,
    )

    return result.text


def translate_script_batch(
    texts: List[str],
    target_lang: str,
    source_lang: str = None,
    preserve_formatting: bool = True,
) -> List[str]:
    translator = get_deepl_client()

    results = translator.translate_text(
        texts,
        source_lang=source_lang if source_lang else None,
        target_lang=target_lang.upper(),
        preserve_formatting=preserve_formatting,
    )

    return [r.text for r in results]


def detect_source_language(text: str) -> str:
    translator = get_deepl_client()
    usage = translator.get_usage()
    result = translator.translate_text(text, target_lang="EN")
    return (
        result.detected_source_lang
        if hasattr(result, "detected_source_lang")
        else DEEPL_DEFAULT_SOURCE_LANG
    )
