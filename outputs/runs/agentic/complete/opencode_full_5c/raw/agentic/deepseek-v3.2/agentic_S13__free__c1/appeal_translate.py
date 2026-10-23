import os
from typing import Dict, Any, Optional
from safety_client import SafetyClient


def appeal_translate(
    appeal_text: str, target_language: str = "en", source_language: Optional[str] = None
) -> Dict[str, Any]:
    """
    Translate appeal text for review.

    Args:
        appeal_text: The appeal text to translate
        target_language: Target language code (default: "en" for English)
        source_language: Optional source language code (auto-detected if not provided)

    Returns:
        Dictionary with translation results
    """
    client = SafetyClient.get_client()

    # Use Google Cloud Translation API
    from google.cloud import translate_v2 as translate

    # Initialize translation client
    translate_client = translate.Client()

    try:
        # Translate the text
        if source_language:
            result = translate_client.translate(
                appeal_text,
                target_language=target_language,
                source_language=source_language,
            )
        else:
            result = translate_client.translate(
                appeal_text, target_language=target_language
            )

        # Extract translation details
        translated_text = result["translatedText"]
        detected_source_language = result.get("detectedSourceLanguage", source_language)

        # Get confidence if available
        confidence = None
        if "confidence" in result:
            confidence = result["confidence"]

        # Optional: Check if translation might have safety issues
        # by translating back to source to verify meaning preservation
        if detected_source_language and detected_source_language != target_language:
            back_translation = translate_client.translate(
                translated_text,
                target_language=detected_source_language,
                source_language=target_language,
            )

            back_translated_text = back_translation["translatedText"]
        else:
            back_translated_text = None

        return {
            "original_text": appeal_text,
            "translated_text": translated_text,
            "source_language": detected_source_language,
            "target_language": target_language,
            "confidence": confidence,
            "back_translation": back_translated_text,
            "provider": "google_translate",
            "model": "google-translate-v2",
        }

    except Exception as e:
        # Fallback to DeepL if Google Translation fails
        try:
            import deepl

            deepl_api_key = os.getenv("DEEPL_API_KEY")
            if not deepl_api_key:
                raise ValueError("DEEPL_API_KEY not configured")

            translator = deepl.Translator(deepl_api_key)

            result = translator.translate_text(
                appeal_text,
                target_lang=target_language.upper(),
                source_lang=source_language.upper() if source_language else None,
            )

            return {
                "original_text": appeal_text,
                "translated_text": result.text,
                "source_language": source_language or "auto",
                "target_language": target_language,
                "confidence": None,  # DeepL doesn't provide confidence scores
                "back_translation": None,
                "provider": "deepl",
                "model": "deepl-translate",
            }

        except Exception as deepl_error:
            return {
                "original_text": appeal_text,
                "translated_text": appeal_text,  # Return original as fallback
                "source_language": source_language or "unknown",
                "target_language": target_language,
                "error": f"Translation failed: {str(e)}, DeepL fallback also failed: {str(deepl_error)}",
                "provider": "none",
                "model": "none",
            }
