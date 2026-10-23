import os
import json
from typing import Dict, Any, List
from google.cloud import translate_v2 as translate


def record_translate(
    document: Dict[str, Any],
    target_language: str = "en",
    fields_to_translate: List[str] = None,
) -> Dict[str, Any]:
    """
    Translate user-facing document fields using Google Cloud Translation API.

    Args:
        document: Document containing fields to translate
        target_language: Target language code (e.g., "en", "es", "fr")
        fields_to_translate: List of field names to translate (defaults to all string fields)

    Returns:
        dict: Translated document with original fields preserved
    """
    client = translate.Client.from_service_account_json(
        os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    )

    if fields_to_translate is None:
        # Translate all string fields
        fields_to_translate = []
        for key, value in document.items():
            if isinstance(value, str) and len(value.strip()) > 0:
                fields_to_translate.append(key)

    translated_doc = document.copy()
    translation_results = {
        "original_language": "auto-detected",
        "target_language": target_language,
        "translated_fields": [],
        "translation_errors": [],
        "character_count": 0,
    }

    for field in fields_to_translate:
        if field not in document:
            continue

        field_value = document[field]
        if not isinstance(field_value, str) or not field_value.strip():
            continue

        try:
            # Detect language first
            detection_result = client.detect_language(field_value)
            detected_language = detection_result["language"]

            # Translate if not already in target language
            if detected_language != target_language:
                translation_result = client.translate(
                    field_value,
                    target_language=target_language,
                    source_language=detected_language,
                )

                translated_text = translation_result["translatedText"]
                translated_doc[f"{field}_translated"] = translated_text

                translation_results["translated_fields"].append(
                    {
                        "field": field,
                        "original": field_value[:100] + "..."
                        if len(field_value) > 100
                        else field_value,
                        "translated": translated_text[:100] + "..."
                        if len(translated_text) > 100
                        else translated_text,
                        "source_language": detected_language,
                        "confidence": detection_result.get("confidence", 0.0),
                    }
                )

                translation_results["character_count"] += len(field_value)

            else:
                # Already in target language
                translation_results["translated_fields"].append(
                    {
                        "field": field,
                        "note": "Already in target language",
                        "source_language": detected_language,
                    }
                )

        except Exception as e:
            error_info = {
                "field": field,
                "error": str(e),
                "text_sample": field_value[:50] + "..."
                if len(field_value) > 50
                else field_value,
            }
            translation_results["translation_errors"].append(error_info)

    # Add translation metadata to document
    translated_doc["_translation_metadata"] = translation_results

    return translated_doc
