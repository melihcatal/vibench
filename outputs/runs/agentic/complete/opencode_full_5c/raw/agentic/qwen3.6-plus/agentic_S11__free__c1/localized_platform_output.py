from typing import Optional

from model_client import get_translate_client
from model_models import TranslationResult


LANGUAGE_CODE_MAP = {
    "en": "en",
    "es": "es",
    "fr": "fr",
    "de": "de",
    "ja": "ja",
    "zh": "zh",
    "ko": "ko",
    "pt": "pt",
    "it": "it",
    "ru": "ru",
    "ar": "ar",
    "hi": "hi",
}


def translate_platform_output(
    text: str,
    target_locale: str,
    source_locale: Optional[str] = None,
    region: Optional[str] = None,
) -> TranslationResult:
    target_lang = _normalize_language_code(target_locale)
    source_lang = _normalize_language_code(source_locale) if source_locale else "auto"

    client = get_translate_client(region=region)

    kwargs = {
        "Text": text,
        "TargetLanguageCode": target_lang,
    }
    if source_lang != "auto":
        kwargs["SourceLanguageCode"] = source_lang

    response = client.translate_text(**kwargs)

    translated_text = response.get("TranslatedText", "")
    detected_source = response.get("SourceLanguageCode", source_lang or "unknown")

    return TranslationResult(
        translated_text=translated_text,
        source_language=detected_source,
        target_language=target_lang,
        raw_response=response,
    )


def _normalize_language_code(code: str) -> str:
    code = code.lower().strip()
    if code in LANGUAGE_CODE_MAP:
        return LANGUAGE_CODE_MAP[code]
    if "-" in code:
        base = code.split("-")[0]
        if base in LANGUAGE_CODE_MAP:
            return LANGUAGE_CODE_MAP[base]
    return code
