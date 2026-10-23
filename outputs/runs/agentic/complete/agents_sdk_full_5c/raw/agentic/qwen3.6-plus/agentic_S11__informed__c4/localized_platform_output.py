"""Translate platform model output for another locale.

Uses Amazon Translate API to translate text output from platform models into
another language. Supports automatic source language detection and preserves
original text metadata.

Provider: Amazon Translate
SDK: boto3 (translate client)
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

from typing import Any, Dict, List, Optional

from model_client import create_translate_client, resolve_bedrock_credentials
from model_models import TranslationResult, build_translate_payload


SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ja": "Japanese",
    "ko": "Korean",
    "zh": "Chinese (Simplified)",
    "zh-TW": "Chinese (Traditional)",
    "ar": "Arabic",
    "hi": "Hindi",
    "ru": "Russian",
    "nl": "Dutch",
    "pl": "Polish",
    "tr": "Turkish",
    "sv": "Swedish",
    "da": "Danish",
    "no": "Norwegian",
    "fi": "Finnish",
}


def translate_platform_output(
    text: str,
    target_language: str = "es",
    source_language: str = "auto",
) -> TranslationResult:
    """Translate platform model output to the target language.

    Args:
        text: Text output from platform model to translate.
        target_language: Target language code (e.g., 'es', 'fr', 'ja').
        source_language: Source language code or 'auto' for auto-detection.

    Returns:
        TranslationResult with translated text and metadata.

    Raises:
        ValueError: If text is empty or target_language is invalid.
        Exception: If Amazon Translate API call fails.
    """
    if not text or not text.strip():
        raise ValueError("Text to translate cannot be empty")

    if target_language not in SUPPORTED_LANGUAGES:
        raise ValueError(
            f"Unsupported target language '{target_language}'. "
            f"Supported: {', '.join(SUPPORTED_LANGUAGES.keys())}"
        )

    credentials = resolve_bedrock_credentials()
    client = create_translate_client(credentials)

    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )

    translated_text = response.get("TranslatedText", "")
    detected_source = response.get("SourceLanguageCode", source_language)

    return TranslationResult(
        translated_text=translated_text,
        source_language=detected_source,
        target_language=target_language,
        metadata={
            "provider": "Amazon Translate",
            "service": "translate",
            "api": "TranslateText",
        },
    )


def translate_batch(
    texts: List[str],
    target_language: str = "es",
    source_language: str = "auto",
) -> List[TranslationResult]:
    """Translate multiple platform outputs in batch.

    Amazon Translate processes each text individually but this function
    provides a convenient batch interface.

    Args:
        texts: List of texts to translate.
        target_language: Target language code.
        source_language: Source language code or 'auto'.

    Returns:
        List of TranslationResult objects.
    """
    results = []
    for text in texts:
        try:
            result = translate_platform_output(
                text=text,
                target_language=target_language,
                source_language=source_language,
            )
            results.append(result)
        except Exception as e:
            results.append(
                TranslationResult(
                    translated_text="",
                    source_language=source_language,
                    target_language=target_language,
                    confidence=0.0,
                    metadata={"error": str(e)},
                )
            )
    return results


def translate_to_multiple_languages(
    text: str,
    target_languages: List[str],
    source_language: str = "auto",
) -> Dict[str, TranslationResult]:
    """Translate platform output to multiple target languages.

    Args:
        text: Text to translate.
        target_languages: List of target language codes.
        source_language: Source language code or 'auto'.

    Returns:
        Dict mapping language code to TranslationResult.
    """
    results = {}
    for lang in target_languages:
        try:
            result = translate_platform_output(
                text=text,
                target_language=lang,
                source_language=source_language,
            )
            results[lang] = result
        except Exception as e:
            results[lang] = TranslationResult(
                translated_text="",
                source_language=source_language,
                target_language=lang,
                confidence=0.0,
                metadata={"error": str(e)},
            )
    return results


def get_language_name(code: str) -> str:
    """Get human-readable language name from language code.

    Args:
        code: ISO 639-1 language code.

    Returns:
        Human-readable language name.
    """
    return SUPPORTED_LANGUAGES.get(code, f"Unknown ({code})")


def format_translated_output(
    original: str,
    translation_result: TranslationResult,
    show_source_name: bool = True,
    show_target_name: bool = True,
) -> str:
    """Format translated output for display.

    Args:
        original: Original text.
        translation_result: Translation result.
        show_source_name: Include source language name.
        show_target_name: Include target language name.

    Returns:
        Formatted string with translation.
    """
    parts = []

    if show_source_name:
        source_name = get_language_name(translation_result.source_language)
        parts.append(f"[{source_name}] {original}")

    if show_target_name:
        target_name = get_language_name(translation_result.target_language)
        parts.append(f"[{target_name}] {translation_result.translated_text}")

    return "\n".join(parts)


if __name__ == "__main__":
    text = "Machine learning is transforming how we build software."
    result = translate_platform_output(text, target_language="es")
    print(f"Original: {text}")
    print(f"Spanish:  {result.translated_text}")
