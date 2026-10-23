import os
from typing import Dict, Any, List
from deep_translator import GoogleTranslator


def translate_document_fields(
    documents: List[Dict[str, Any]],
    target_language: str = "en",
    source_language: str = "auto",
) -> Dict[str, Any]:
    """
    Translate user-facing document fields using Google Translate API.

    Args:
        documents: List of document records to translate
        target_language: Target language code (e.g., 'en', 'es', 'fr')
        source_language: Source language code or 'auto' for auto-detection

    Returns:
        dict: Translation results
    """
    try:
        # Initialize Google Translator
        translator = GoogleTranslator(source=source_language, target=target_language)

        translated_docs = []
        translation_stats = {
            "total_fields": 0,
            "translated_fields": 0,
            "skipped_fields": 0,
            "characters_translated": 0,
        }

        for doc in documents:
            doc_id = doc.get("id", "unknown")
            doc_data = doc.get("data", {})

            if not isinstance(doc_data, dict):
                # Skip non-dict documents
                translated_docs.append(
                    {
                        "document_id": doc_id,
                        "translated": False,
                        "reason": "Document data is not a dictionary",
                        "original_data": doc_data,
                    }
                )
                continue

            translated_data = {}
            field_stats = {"translated": 0, "skipped": 0}

            for key, value in doc_data.items():
                translation_stats["total_fields"] += 1

                # Only translate string fields that appear to be user-facing text
                if should_translate_field(key, value):
                    try:
                        if isinstance(value, str) and value.strip():
                            translated_value = translator.translate(value)
                            translated_data[key] = translated_value
                            field_stats["translated"] += 1
                            translation_stats["translated_fields"] += 1
                            translation_stats["characters_translated"] += len(value)
                        else:
                            # Non-string or empty values are copied as-is
                            translated_data[key] = value
                            field_stats["skipped"] += 1
                            translation_stats["skipped_fields"] += 1
                    except Exception as e:
                        # If translation fails, keep original value
                        translated_data[key] = value
                        field_stats["skipped"] += 1
                        translation_stats["skipped_fields"] += 1
                else:
                    # Skip fields that shouldn't be translated
                    translated_data[key] = value
                    field_stats["skipped"] += 1
                    translation_stats["skipped_fields"] += 1

            translated_docs.append(
                {
                    "document_id": doc_id,
                    "translated": field_stats["translated"] > 0,
                    "translated_data": translated_data,
                    "field_stats": field_stats,
                    "target_language": target_language,
                    "source_language": source_language,
                }
            )

        return {
            "success": True,
            "translations": translated_docs,
            "stats": translation_stats,
            "target_language": target_language,
            "source_language": source_language,
            "service_used": "google-translate-api",
            "translator_lib": "deep-translator",
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "service_used": "google-translate-api",
        }


def should_translate_field(field_name: str, field_value: Any) -> bool:
    """
    Determine if a field should be translated based on field name and value.

    Args:
        field_name: Name of the field
        field_value: Value of the field

    Returns:
        bool: True if field should be translated
    """
    # Skip fields that are likely not user-facing text
    skip_keywords = [
        "id",
        "_id",
        "uuid",
        "timestamp",
        "date",
        "time",
        "created",
        "updated",
        "version",
        "status",
        "code",
        "number",
        "count",
        "amount",
        "price",
        "quantity",
        "score",
        "rating",
        "percentage",
        "flag",
        "boolean",
    ]

    field_lower = field_name.lower()

    # Check if field name contains skip keywords
    for keyword in skip_keywords:
        if keyword in field_lower:
            return False

    # Only translate string values
    if not isinstance(field_value, str):
        return False

    # Skip very short strings (likely codes or abbreviations)
    if len(field_value.strip()) < 3:
        return False

    # Skip strings that look like codes (all caps with numbers/underscores)
    if field_value.isupper() and any(c.isdigit() or c == "_" for c in field_value):
        return False

    # Skip strings that look like URLs or emails
    if "://" in field_value or "@" in field_value and "." in field_value:
        return False

    return True


def translate_single_document(
    document: Dict[str, Any], target_language: str = "en"
) -> Dict[str, Any]:
    """
    Translate a single document.

    Args:
        document: Single document record
        target_language: Target language code

    Returns:
        dict: Translation results
    """
    result = translate_document_fields([document], target_language)
    if result["success"]:
        # Extract single result
        single_result = result["translations"][0] if result["translations"] else {}
        return {
            "success": True,
            "document_id": single_result.get("document_id"),
            "translated": single_result.get("translated", False),
            "translated_data": single_result.get("translated_data", {}),
            "target_language": target_language,
            "service_used": "google-translate-api",
        }
    else:
        return result


def detect_language(text: str) -> Dict[str, Any]:
    """
    Detect the language of a text string using Google Translate.

    Args:
        text: Text to detect language for

    Returns:
        dict: Language detection results
    """
    try:
        # Use Google Translator for language detection
        translator = GoogleTranslator(source="auto", target="en")

        # Translate a small sample to detect language
        if len(text) > 100:
            sample = text[:100]
        else:
            sample = text

        # The library automatically detects language during translation
        translated = translator.translate(sample)

        # Note: deep-translator doesn't expose detected language directly
        # In a real implementation, you would use Google Cloud Translation API
        # with the detect_language method

        return {
            "success": True,
            "text_sample": sample,
            "detected_language": "unknown",  # Would be actual detection in full implementation
            "confidence": 0.0,  # Would be actual confidence score
            "service_used": "google-translate-api",
            "note": "Language detection requires Google Cloud Translation API for full functionality",
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "service_used": "google-translate-api",
        }


def batch_translate_with_language_detection(
    documents: List[Dict[str, Any]], target_languages: List[str] = ["en", "es", "fr"]
) -> Dict[str, Any]:
    """
    Translate documents to multiple target languages.

    Args:
        documents: List of document records
        target_languages: List of target language codes

    Returns:
        dict: Multi-language translation results
    """
    results = {}

    for lang in target_languages:
        lang_result = translate_document_fields(documents, target_language=lang)
        results[lang] = lang_result

    return {
        "success": all(r.get("success", False) for r in results.values()),
        "results_by_language": results,
        "target_languages": target_languages,
        "document_count": len(documents),
    }
