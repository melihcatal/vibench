import os
from typing import List, Dict, Any
import deepl
from identity_models import TranslationResult


def translate_consent_text(
    text: str,
    target_language: str = "EN",
    source_language: str | None = None,
    auth_key: str | None = None,
    formality: str | None = None,
) -> TranslationResult:
    if auth_key is None:
        auth_key = os.getenv("DEEPL_AUTH_KEY", "")

    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    translate_kwargs: Dict[str, Any] = {
        "target_lang": target_language,
    }
    if source_language:
        translate_kwargs["source_lang"] = source_language
    if formality:
        translate_kwargs["formality"] = formality

    result = translator.translate_text(text, **translate_kwargs)

    detected_source = (
        result.detected_source_lang if hasattr(result, "detected_source_lang") else ""
    )

    return TranslationResult(
        source_text=text,
        translated_text=result.text,
        source_language=detected_source,
        target_language=target_language,
        confidence=1.0,
    )


def translate_consent_batch(
    texts: List[str],
    target_language: str = "EN",
    source_language: str | None = None,
    auth_key: str | None = None,
    formality: str | None = None,
) -> List[TranslationResult]:
    if auth_key is None:
        auth_key = os.getenv("DEEPL_AUTH_KEY", "")

    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    translate_kwargs: Dict[str, Any] = {
        "target_lang": target_language,
    }
    if source_language:
        translate_kwargs["source_lang"] = source_language
    if formality:
        translate_kwargs["formality"] = formality

    results = translator.translate_text(texts, **translate_kwargs)

    if isinstance(results, list):
        return [
            TranslationResult(
                source_text=orig,
                translated_text=tr.text,
                source_language=tr.detected_source_lang
                if hasattr(tr, "detected_source_lang")
                else "",
                target_language=target_language,
                confidence=1.0,
            )
            for orig, tr in zip(texts, results)
        ]
    else:
        return [
            TranslationResult(
                source_text=texts[0] if texts else "",
                translated_text=results.text,
                source_language=results.detected_source_lang
                if hasattr(results, "detected_source_lang")
                else "",
                target_language=target_language,
                confidence=1.0,
            )
        ]


def translate_idp_consent_copy(
    consent_text: str,
    provider: str = "auth0",
    target_languages: List[str] | None = None,
    auth_key: str | None = None,
) -> Dict[str, Any]:
    if target_languages is None:
        target_languages = ["EN", "ES", "FR", "DE", "JA", "ZH"]

    translations = {}
    for lang in target_languages:
        try:
            result = translate_consent_text(
                text=consent_text,
                target_language=lang,
                auth_key=auth_key,
                formality="default",
            )
            translations[lang] = result.to_dict()
        except Exception as e:
            translations[lang] = {"error": str(e), "source_text": consent_text}

    return {
        "original_text": consent_text,
        "provider": provider,
        "translations": translations,
        "translator_service": "deepl",
    }


if __name__ == "__main__":
    sample_consent = "By continuing, you agree to share your profile information with this application."
    result = translate_consent_text(sample_consent, target_language="ES")
    print(f"Original: {result.source_text}")
    print(f"Translated: {result.translated_text}")
    print(f"Service: deepl")
