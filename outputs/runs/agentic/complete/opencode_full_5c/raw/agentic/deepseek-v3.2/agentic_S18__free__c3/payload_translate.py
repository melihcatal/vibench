import os
import json
from typing import Dict, Any, Optional
from google.cloud import translate_v2 as translate


def translate_message_payload(message_data, target_language="en", source_language=None):
    """Translate customer-facing message payload text using Google Cloud Translation API."""

    # Initialize the Translation API client
    client = translate.Client()

    # Extract text fields from message data
    text_fields = extract_text_fields(message_data)

    if not text_fields:
        return {
            "original": message_data,
            "translated": message_data,
            "target_language": target_language,
            "source_language": "auto",
            "translated_fields": [],
            "provider": "google_cloud_translation",
        }

    # Translate each text field
    translated_fields = {}
    translation_details = []

    for field_path, text in text_fields.items():
        if not text or not isinstance(text, str):
            translated_fields[field_path] = text
            continue

        # Perform translation
        try:
            result = client.translate(
                text,
                target_language=target_language,
                source_language=source_language,
                format_="text",
            )

            translated_fields[field_path] = result["translatedText"]

            translation_details.append(
                {
                    "field": field_path,
                    "original": text[:200] + ("..." if len(text) > 200 else ""),
                    "translated": result["translatedText"][:200]
                    + ("..." if len(result["translatedText"]) > 200 else ""),
                    "detected_source_language": result.get(
                        "detectedSourceLanguage", source_language
                    ),
                    "model": result.get(
                        "model", "nmt"
                    ),  # Neural Machine Translation model
                }
            )

        except Exception as e:
            # If translation fails, keep original text
            translated_fields[field_path] = text
            translation_details.append(
                {
                    "field": field_path,
                    "error": str(e),
                    "original": text[:200] + ("..." if len(text) > 200 else ""),
                    "translated": text[:200] + ("..." if len(text) > 200 else ""),
                    "note": "Translation failed, using original text",
                }
            )

    # Create translated message by replacing text fields
    translated_message = replace_text_fields(message_data, translated_fields)

    # Determine source language from translations
    detected_languages = [
        detail.get("detected_source_language")
        for detail in translation_details
        if detail.get("detected_source_language")
    ]

    if detected_languages:
        source_language = max(set(detected_languages), key=detected_languages.count)
    else:
        source_language = "unknown"

    return {
        "original": message_data,
        "translated": translated_message,
        "target_language": target_language,
        "source_language": source_language,
        "translation_details": translation_details,
        "translated_field_count": len(
            [d for d in translation_details if "error" not in d]
        ),
        "failed_translations": len([d for d in translation_details if "error" in d]),
        "provider": "google_cloud_translation",
        "model": "nmt",  # Neural Machine Translation
    }


def extract_text_fields(data, parent_key=""):
    """Recursively extract all text fields from nested data structure."""
    text_fields = {}

    if isinstance(data, dict):
        for key, value in data.items():
            new_key = f"{parent_key}.{key}" if parent_key else key
            if isinstance(value, str) and is_translatable_text(value, key):
                text_fields[new_key] = value
            elif isinstance(value, (dict, list)):
                text_fields.update(extract_text_fields(value, new_key))

    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_key = f"{parent_key}[{i}]" if parent_key else f"[{i}]"
            if isinstance(item, str) and is_translatable_text(item, str(i)):
                text_fields[new_key] = item
            elif isinstance(item, (dict, list)):
                text_fields.update(extract_text_fields(item, new_key))

    elif isinstance(data, str) and is_translatable_text(data, parent_key):
        text_fields[parent_key] = data

    return text_fields


def is_translatable_text(text, field_name):
    """Determine if text should be translated."""
    # Skip very short text
    if len(text.strip()) < 3:
        return False

    # Skip numeric strings
    if text.strip().replace(".", "", 1).replace(",", "").isdigit():
        return False

    # Skip field names that indicate non-translatable content
    non_translatable_fields = [
        "id",
        "uuid",
        "timestamp",
        "date",
        "url",
        "email",
        "phone",
        "zipcode",
        "postalcode",
        "code",
        "sku",
    ]

    field_lower = field_name.lower()
    for non_field in non_translatable_fields:
        if non_field in field_lower:
            return False

    # Skip text that looks like codes or IDs
    if text.strip().startswith(("#", "@", "http://", "https://")):
        return False

    return True


def replace_text_fields(original_data, translated_fields):
    """Replace text fields in original data with translated versions."""
    if not translated_fields:
        return original_data

    if isinstance(original_data, dict):
        result = {}
        for key, value in original_data.items():
            field_path = key
            if field_path in translated_fields:
                result[key] = translated_fields[field_path]
            elif isinstance(value, (dict, list)):
                # Handle nested structures
                nested_fields = {
                    k.replace(f"{field_path}.", "", 1): v
                    for k, v in translated_fields.items()
                    if k.startswith(f"{field_path}.")
                }
                if nested_fields:
                    result[key] = replace_text_fields(value, nested_fields)
                else:
                    result[key] = value
            else:
                result[key] = value
        return result

    elif isinstance(original_data, list):
        result = []
        for i, item in enumerate(original_data):
            field_path = f"[{i}]"
            if field_path in translated_fields:
                result.append(translated_fields[field_path])
            elif isinstance(item, (dict, list)):
                # Handle nested structures
                nested_fields = {
                    k.replace(field_path, "", 1).lstrip("."): v
                    for k, v in translated_fields.items()
                    if k.startswith(field_path)
                }
                if nested_fields:
                    result.append(replace_text_fields(item, nested_fields))
                else:
                    result.append(item)
            else:
                result.append(item)
        return result

    else:
        return original_data


def detect_language(text):
    """Detect the language of text using Google Cloud Translation API."""
    if not text or not isinstance(text, str) or len(text.strip()) < 3:
        return {"language": "unknown", "confidence": 0.0}

    client = translate.Client()

    try:
        result = client.detect_language(text)
        return {
            "language": result["language"],
            "confidence": result["confidence"],
            "provider": "google_cloud_translation",
        }
    except Exception as e:
        return {"language": "unknown", "confidence": 0.0, "error": str(e)}


def translate_batch(messages, target_language="en"):
    """Translate a batch of messages."""
    results = []

    for i, message in enumerate(messages):
        try:
            translation_result = translate_message_payload(message, target_language)
            results.append({"index": i, "success": True, "result": translation_result})
        except Exception as e:
            results.append(
                {"index": i, "success": False, "error": str(e), "message": message}
            )

    return {
        "total_messages": len(messages),
        "successful_translations": len([r for r in results if r["success"]]),
        "failed_translations": len([r for r in results if not r["success"]]),
        "results": results,
        "target_language": target_language,
        "provider": "google_cloud_translation",
    }


if __name__ == "__main__":
    # Example usage
    sample_message = {
        "user_id": "12345",
        "name": "Juan Pérez",
        "comment": "¡Hola! Me encanta este servicio. Es muy útil para mis necesidades diarias.",
        "rating": 5,
        "metadata": {"category": "feedback", "tags": ["positive", "spanish"]},
    }

    result = translate_message_payload(sample_message, "en")
    print(f"Translation result: {json.dumps(result, indent=2)}")
