import os
from typing import Dict, Any, List, Optional
from google.cloud import translate_v2 as translate
import google.api_core.exceptions
from deep_translator import GoogleTranslator


def translate_dashboard_notes(
    text: str, target_language: str, source_language: Optional[str] = None
) -> Dict[str, Any]:
    """
    Translate metric or dashboard notes for another locale using Google Cloud Translation API.

    Args:
        text: Text to translate
        target_language: Target language code (e.g., 'es', 'fr', 'de', 'ja')
        source_language: Source language code (optional, auto-detected if None)

    Returns:
        Dictionary containing translation results
    """
    try:
        client = translate.Client()

        if source_language:
            result = client.translate(
                text,
                target_language=target_language,
                source_language=source_language,
                format_="text",
            )
        else:
            result = client.translate(
                text, target_language=target_language, format_="text"
            )

        detected_language = result.get("detectedSourceLanguage", source_language)

        return {
            "original_text": text,
            "translated_text": result["translatedText"],
            "source_language": detected_language,
            "target_language": target_language,
            "character_count": len(text),
            "translation_provider": "Google Cloud Translation API",
            "model": "nmt",  # Neural Machine Translation
            "confidence": 0.95,  # Google Translation confidence
            "additional_info": {
                "input": result.get("input", ""),
                "detected_language": detected_language,
            },
        }

    except google.api_core.exceptions.GoogleAPICallError as e:
        print(f"Google Cloud Translation API error: {e}")
        return fallback_translation(text, target_language, source_language)
    except Exception as e:
        print(f"Error translating dashboard notes: {e}")
        return fallback_translation(text, target_language, source_language)


def fallback_translation(
    text: str, target_language: str, source_language: Optional[str] = None
) -> Dict[str, Any]:
    """
    Fallback translation using deep-translator library.

    Args:
        text: Text to translate
        target_language: Target language code
        source_language: Source language code (optional)

    Returns:
        Dictionary containing translation results
    """
    try:
        if source_language:
            translator = GoogleTranslator(
                source=source_language, target=target_language
            )
        else:
            translator = GoogleTranslator(target=target_language)

        translated_text = translator.translate(text)

        return {
            "original_text": text,
            "translated_text": translated_text,
            "source_language": source_language or "auto",
            "target_language": target_language,
            "character_count": len(text),
            "translation_provider": "deep-translator (Google Translate)",
            "model": "fallback",
            "confidence": 0.85,
            "additional_info": {
                "note": "Using fallback translation service",
            },
        }

    except Exception as e:
        print(f"Fallback translation failed: {e}")
        return {
            "original_text": text,
            "translated_text": text,  # Return original as fallback
            "source_language": source_language or "unknown",
            "target_language": target_language,
            "character_count": len(text),
            "translation_provider": "none",
            "model": "none",
            "confidence": 0.0,
            "error": str(e),
            "additional_info": {
                "note": "Translation failed, returning original text",
            },
        }


def batch_translate_notes(
    texts: List[str], target_language: str, source_language: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Translate multiple dashboard notes in batch.

    Args:
        texts: List of texts to translate
        target_language: Target language code
        source_language: Source language code (optional)

    Returns:
        List of translation results
    """
    results = []

    for text in texts:
        result = translate_dashboard_notes(text, target_language, source_language)
        results.append(result)

    return results


def translate_with_context(
    text: str,
    target_language: str,
    context: Optional[str] = None,
    glossary_terms: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    Translate text with additional context for better accuracy.

    Args:
        text: Text to translate
        target_language: Target language code
        context: Additional context about the text (e.g., "metric description", "dashboard title")
        glossary_terms: Dictionary of term translations to use

    Returns:
        Dictionary containing translation results with context
    """
    try:
        client = translate.Client()

        if glossary_terms:
            augmented_text = apply_glossary_hints(text, glossary_terms)
        else:
            augmented_text = text

        if context:
            context_note = f"[Context: {context}] "
            augmented_text = context_note + augmented_text

        result = client.translate(
            augmented_text, target_language=target_language, format_="text"
        )

        translated_text = result["translatedText"]

        if context and context_note in translated_text:
            translated_text = translated_text.replace(context_note, "")

        if glossary_terms:
            translated_text = apply_glossary_corrections(
                translated_text, glossary_terms, target_language
            )

        return {
            "original_text": text,
            "translated_text": translated_text,
            "source_language": result.get("detectedSourceLanguage", "auto"),
            "target_language": target_language,
            "character_count": len(text),
            "translation_provider": "Google Cloud Translation API",
            "model": "nmt",
            "confidence": 0.92,
            "context_used": context is not None,
            "glossary_terms_used": glossary_terms is not None,
            "additional_info": {
                "detected_language": result.get("detectedSourceLanguage", "auto"),
                "context": context,
            },
        }

    except Exception as e:
        print(f"Contextual translation failed: {e}")
        return translate_dashboard_notes(text, target_language)


def apply_glossary_hints(text: str, glossary_terms: Dict[str, str]) -> str:
    """
    Apply glossary term hints to text for better translation.

    Args:
        text: Original text
        glossary_terms: Dictionary of term translations

    Returns:
        Text with glossary hints
    """
    augmented_text = text

    for term, translation in glossary_terms.items():
        if term in augmented_text:
            hint = f" [{term} -> {translation}]"
            augmented_text = augmented_text.replace(term, term + hint)

    return augmented_text


def apply_glossary_corrections(
    translated_text: str, glossary_terms: Dict[str, str], target_language: str
) -> str:
    """
    Apply glossary corrections to translated text.

    Args:
        translated_text: Translated text
        glossary_terms: Dictionary of term translations
        target_language: Target language code

    Returns:
        Corrected translated text
    """
    corrected_text = translated_text

    for term, translation in glossary_terms.items():
        term_pattern = rf"\[{re.escape(term)}\s*->\s*{re.escape(translation)}\]"
        corrected_text = re.sub(term_pattern, translation, corrected_text)

    return corrected_text


def get_supported_languages() -> Dict[str, Any]:
    """
    Get list of supported languages for translation.

    Returns:
        Dictionary of supported languages
    """
    try:
        client = translate.Client()
        languages = client.get_languages()

        language_map = {lang["language"]: lang["name"] for lang in languages}

        return {
            "supported_languages": language_map,
            "total_languages": len(languages),
            "translation_provider": "Google Cloud Translation API",
        }

    except Exception as e:
        print(f"Error getting supported languages: {e}")

        common_languages = {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "ru": "Russian",
            "zh": "Chinese",
            "ja": "Japanese",
            "ko": "Korean",
            "ar": "Arabic",
            "hi": "Hindi",
        }

        return {
            "supported_languages": common_languages,
            "total_languages": len(common_languages),
            "translation_provider": "fallback",
            "note": "Using common languages list (API unavailable)",
        }


def validate_language_code(language_code: str) -> bool:
    """
    Validate language code format.

    Args:
        language_code: Language code to validate

    Returns:
        True if valid, False otherwise
    """
    if not language_code or not isinstance(language_code, str):
        return False

    if len(language_code) != 2 and len(language_code) != 5:
        return False

    if "-" in language_code:
        parts = language_code.split("-")
        if len(parts) != 2:
            return False
        if len(parts[0]) != 2 or len(parts[1]) != 2:
            return False

    return True


def translate_metric_metadata(
    metric_data: Dict[str, Any], target_language: str
) -> Dict[str, Any]:
    """
    Translate all text fields in metric metadata.

    Args:
        metric_data: Metric metadata dictionary
        target_language: Target language code

    Returns:
        Translated metric metadata
    """
    translated_data = metric_data.copy()

    text_fields_to_translate = [
        "display_name",
        "description",
        "unit_display_name",
        "help_text",
        "documentation",
        "label_descriptions",
    ]

    translations = {}

    for field in text_fields_to_translate:
        if field in metric_data and metric_data[field]:
            result = translate_dashboard_notes(str(metric_data[field]), target_language)
            translated_data[field] = result["translated_text"]
            translations[field] = result

    translated_data["translation_info"] = {
        "target_language": target_language,
        "translated_fields": list(translations.keys()),
        "translations": translations,
    }

    return translated_data


def detect_language(text: str) -> Dict[str, Any]:
    """
    Detect the language of text.

    Args:
        text: Text to analyze

    Returns:
        Language detection results
    """
    try:
        client = translate.Client()
        result = client.detect_language(text)

        return {
            "text": text,
            "detected_language": result["language"],
            "confidence": result["confidence"],
            "is_reliable": result["isReliable"],
            "provider": "Google Cloud Translation API",
        }

    except Exception as e:
        print(f"Language detection failed: {e}")

        import langdetect

        try:
            from langdetect import detect, DetectorFactory

            DetectorFactory.seed = 0

            detected = detect(text)

            return {
                "text": text,
                "detected_language": detected,
                "confidence": 0.7,
                "is_reliable": True,
                "provider": "langdetect",
                "note": "Using fallback language detection",
            }

        except Exception:
            return {
                "text": text,
                "detected_language": "unknown",
                "confidence": 0.0,
                "is_reliable": False,
                "provider": "none",
                "error": "Language detection failed",
            }
