import os
from typing import Dict, Any, Optional
from identity_models import TranslationResult
import deepl


def translate_consent_text(
    text: str, target_language: str, source_language: Optional[str] = None
) -> TranslationResult:
    """Translate identity-provider consent copy using DeepL."""
    auth_key = os.environ.get("DEEPL_AUTH_KEY")

    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable must be set")

    # Initialize DeepL translator
    translator = deepl.Translator(auth_key)

    # Map language codes if needed
    language_map = {
        "en": "EN-US",
        "en-us": "EN-US",
        "en-gb": "EN-GB",
        "es": "ES",
        "fr": "FR",
        "de": "DE",
        "it": "IT",
        "pt": "PT-PT",
        "pt-br": "PT-BR",
        "nl": "NL",
        "pl": "PL",
        "ru": "RU",
        "ja": "JA",
        "zh": "ZH",
        "zh-cn": "ZH",
        "ko": "KO",
    }

    # Normalize target language
    target_lang_norm = target_language.lower()
    if target_lang_norm in language_map:
        target_lang_code = language_map[target_lang_norm]
    else:
        # Try to use as-is or default to English
        target_lang_code = target_language.upper()

    # Handle source language
    source_lang_code = None
    if source_language:
        source_lang_norm = source_language.lower()
        if source_lang_norm in language_map:
            source_lang_code = language_map[source_lang_norm]
        else:
            source_lang_code = source_language.upper()

    try:
        # Translate text using DeepL
        if source_lang_code:
            result = translator.translate_text(
                text, source_lang=source_lang_code, target_lang=target_lang_code
            )
        else:
            # Let DeepL detect source language
            result = translator.translate_text(text, target_lang=target_lang_code)

        # Get detected language if not specified
        detected_language = None
        if not source_language:
            detected_language = result.detected_source_lang.lower()

        # Map back to standard language codes
        reverse_language_map = {v: k for k, v in language_map.items()}
        target_lang_standard = reverse_language_map.get(
            target_lang_code, target_lang_code.lower()
        )

        if detected_language:
            detected_language_standard = reverse_language_map.get(
                detected_language.upper(), detected_language
            )
        else:
            detected_language_standard = source_language

        return TranslationResult(
            translated_text=result.text,
            source_language=detected_language_standard or source_language or "unknown",
            target_language=target_lang_standard,
            detected_language=detected_language_standard,
            confidence=None,  # DeepL doesn't provide confidence scores
        )

    except deepl.DeepLException as e:
        # Handle specific DeepL errors
        error_msg = str(e)

        if "quota exceeded" in error_msg.lower():
            raise ValueError(
                "DeepL translation quota exceeded. Please check your account limits."
            )
        elif "invalid target language" in error_msg.lower():
            raise ValueError(
                f"Invalid target language: {target_language}. Supported languages: {list(language_map.keys())}"
            )
        elif "text too long" in error_msg.lower():
            raise ValueError("Text exceeds DeepL's maximum length limit.")
        else:
            raise ValueError(f"DeepL translation failed: {error_msg}")

    except Exception as e:
        # Fallback: return original text with error note
        return TranslationResult(
            translated_text=f"[TRANSLATION ERROR: {str(e)}] {text}",
            source_language=source_language or "unknown",
            target_language=target_language,
            detected_language=source_language,
            confidence=0.0,
        )


def translate_consent_template(
    template: Dict[str, Any], target_language: str
) -> Dict[str, Any]:
    """Translate a consent template with multiple text fields."""
    translated_template = template.copy()

    # Fields that typically need translation in consent templates
    translatable_fields = [
        "title",
        "description",
        "terms",
        "privacy_policy",
        "accept_button",
        "decline_button",
        "help_text",
        "data_usage",
        "sharing_info",
        "retention_period",
    ]

    for field in translatable_fields:
        if (
            field in template
            and isinstance(template[field], str)
            and template[field].strip()
        ):
            try:
                translation = translate_consent_text(template[field], target_language)
                translated_template[field] = translation.translated_text
            except Exception as e:
                # Keep original text and add error note
                translated_template[field] = (
                    f"[Translation failed: {str(e)}] {template[field]}"
                )

    return translated_template
