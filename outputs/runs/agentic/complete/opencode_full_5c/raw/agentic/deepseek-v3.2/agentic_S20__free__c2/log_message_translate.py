import os
from typing import Dict, List, Any, Optional
from deep_translator import GoogleTranslator


def translate_log_messages(
    log_messages: List[str],
    target_language: str = "es",
    source_language: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate support-visible log messages for another locale using Google Translate.

    Args:
        log_messages: List of log message strings to translate
        target_language: Target language code (e.g., 'es' for Spanish, 'fr' for French)
        source_language: Optional source language code (auto-detected if not provided)

    Returns:
        Dictionary with translation results
    """
    if not log_messages:
        return {
            "summary": "No messages to translate",
            "translated_count": 0,
            "target_language": target_language,
        }

    try:
        # Initialize translator
        translator = GoogleTranslator(
            source=source_language or "auto", target=target_language
        )

        translations = []
        failed_translations = []

        for i, message in enumerate(log_messages):
            if not message or not isinstance(message, str):
                translations.append(
                    {
                        "original_index": i,
                        "original_message": message,
                        "translated_message": message,  # Keep original for non-strings
                        "translation_success": False,
                        "error": "Invalid message type",
                    }
                )
                failed_translations.append(i)
                continue

            try:
                # Translate the message
                translated = translator.translate(message)

                translations.append(
                    {
                        "original_index": i,
                        "original_message": message,
                        "translated_message": translated,
                        "translation_success": True,
                        "source_language": source_language or "auto",
                        "target_language": target_language,
                    }
                )

            except Exception as e:
                # Translation failed, keep original
                translations.append(
                    {
                        "original_index": i,
                        "original_message": message,
                        "translated_message": message,
                        "translation_success": False,
                        "error": str(e),
                        "source_language": source_language or "auto",
                        "target_language": target_language,
                    }
                )
                failed_translations.append(i)

        # Calculate statistics
        successful = len(translations) - len(failed_translations)
        success_rate = (successful / len(translations) * 100) if translations else 0

        # Language code mapping for display
        language_names = {
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "ru": "Russian",
            "zh-CN": "Chinese (Simplified)",
            "ja": "Japanese",
            "ko": "Korean",
            "ar": "Arabic",
        }

        target_language_name = language_names.get(target_language, target_language)

        summary = {
            "total_messages": len(log_messages),
            "successfully_translated": successful,
            "failed_translations": len(failed_translations),
            "success_rate": round(success_rate, 1),
            "target_language": target_language,
            "target_language_name": target_language_name,
            "source_language": source_language or "auto-detected",
            "translation_service": "Google Translate API (via deep-translator)",
            "failed_indices": failed_translations,
        }

        return {"summary": summary, "translations": translations}

    except Exception as e:
        # Fallback if translator initialization fails
        return {
            "summary": {
                "total_messages": len(log_messages),
                "successfully_translated": 0,
                "failed_translations": len(log_messages),
                "success_rate": 0,
                "target_language": target_language,
                "error": f"Translator initialization failed: {str(e)}",
                "translation_service": "Failed to initialize",
            },
            "translations": [
                {
                    "original_index": i,
                    "original_message": msg,
                    "translated_message": msg,
                    "translation_success": False,
                    "error": f"Translator initialization failed: {str(e)}",
                }
                for i, msg in enumerate(log_messages)
            ],
        }


def translate_log_entries(
    log_entries: List[Dict[str, Any]],
    target_language: str = "es",
    fields_to_translate: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Translate specific fields in log entries.

    Args:
        log_entries: List of log entry dictionaries
        target_language: Target language code
        fields_to_translate: List of field names to translate (default: ['message'])

    Returns:
        Dictionary with translated log entries
    """
    if fields_to_translate is None:
        fields_to_translate = ["message"]

    # Extract messages to translate
    messages_to_translate = []
    message_indices = []  # Track which log entry each message belongs to

    for i, entry in enumerate(log_entries):
        for field in fields_to_translate:
            if field in entry and isinstance(entry[field], str):
                messages_to_translate.append(entry[field])
                message_indices.append((i, field))

    # Translate all messages
    translation_results = translate_log_messages(messages_to_translate, target_language)

    # Apply translations back to log entries
    translated_entries = []
    for entry in log_entries:
        translated_entries.append(entry.copy())

    # Map translations back to their original positions
    translation_map = {}
    for idx, (translation, (entry_idx, field)) in enumerate(
        zip(translation_results["translations"], message_indices)
    ):
        if translation["translation_success"]:
            if entry_idx not in translation_map:
                translation_map[entry_idx] = {}
            translation_map[entry_idx][field] = translation["translated_message"]

    # Apply translations
    for entry_idx, field_translations in translation_map.items():
        for field, translated_text in field_translations.items():
            translated_entries[entry_idx][f"{field}_translated"] = translated_text
            translated_entries[entry_idx][f"{field}_translation_lang"] = target_language

    # Add translation metadata to each entry
    for i, entry in enumerate(translated_entries):
        entry["_translation_metadata"] = {
            "target_language": target_language,
            "translated_fields": [f for f in fields_to_translate if f in entry],
            "has_translations": any(
                f"{f}_translated" in entry for f in fields_to_translate
            ),
        }

    return {
        "original_count": len(log_entries),
        "translated_count": len(translation_map),
        "target_language": target_language,
        "fields_translated": fields_to_translate,
        "translation_summary": translation_results["summary"],
        "translated_entries": translated_entries,
    }


def batch_translate_for_support(
    log_entries: List[Dict[str, Any]], support_locale: str = "es"
) -> Dict[str, Any]:
    """
    Batch translate log entries for support team review.

    Args:
        log_entries: List of log entry dictionaries
        support_locale: Locale/language for support team

    Returns:
        Dictionary with support-ready translated logs
    """
    # Fields that are most useful for support teams
    support_fields = ["message", "error_details", "user_message", "description"]

    # Filter to entries that might need translation
    entries_to_translate = []
    for entry in log_entries:
        # Only translate if it has relevant fields with text
        has_translatable_content = any(
            field in entry and isinstance(entry[field], str) and entry[field].strip()
            for field in support_fields
        )

        if has_translatable_content:
            entries_to_translate.append(entry)

    if not entries_to_translate:
        return {
            "summary": "No translatable content found in log entries",
            "support_locale": support_locale,
            "translated_count": 0,
            "total_entries": len(log_entries),
        }

    # Translate the entries
    translation_result = translate_log_entries(
        entries_to_translate,
        target_language=support_locale,
        fields_to_translate=support_fields,
    )

    # Create support-friendly format
    support_entries = []
    for entry in translation_result["translated_entries"]:
        support_entry = {
            "timestamp": entry.get("timestamp"),
            "severity": entry.get("severity"),
            "service": entry.get("service"),
            "original_message": entry.get("message", ""),
            "translated_message": entry.get(
                "message_translated", entry.get("message", "")
            ),
            "correlation_id": entry.get("correlation_id"),
            "additional_info": {},
        }

        # Add other translated fields
        for field in support_fields:
            if field != "message" and field in entry:
                support_entry["additional_info"][f"original_{field}"] = entry[field]
                translated_key = f"{field}_translated"
                if translated_key in entry:
                    support_entry["additional_info"][f"translated_{field}"] = entry[
                        translated_key
                    ]

        support_entries.append(support_entry)

    return {
        "summary": f"Translated {translation_result['translated_count']} log entries for {support_locale} support",
        "support_locale": support_locale,
        "total_entries": len(log_entries),
        "translated_entries": len(entries_to_translate),
        "translation_success_rate": translation_result["translation_summary"][
            "success_rate"
        ],
        "support_ready_entries": support_entries,
        "translation_details": translation_result["translation_summary"],
    }


if __name__ == "__main__":
    # Example usage
    test_logs = [
        {
            "timestamp": "2024-01-15T10:30:00Z",
            "severity": "ERROR",
            "message": "Database connection timeout after 30 seconds",
            "service": "user-service",
            "error_details": "Failed to connect to PostgreSQL database",
        },
        {
            "timestamp": "2024-01-15T10:31:00Z",
            "severity": "INFO",
            "message": "User authentication successful",
            "service": "auth-service",
            "user_message": "Welcome back, user123",
        },
        {
            "timestamp": "2024-01-15T10:32:00Z",
            "severity": "WARNING",
            "message": "High memory usage detected in container",
            "service": "monitoring-service",
            "description": "Memory usage exceeds 85% threshold",
        },
    ]

    # Test single message translation
    test_messages = [
        "Database connection failed",
        "User login successful",
        "System error detected",
    ]
    single_result = translate_log_messages(test_messages, target_language="es")
    print(
        f"Translation to Spanish: {single_result['summary']['success_rate']}% success"
    )

    # Test log entry translation
    entry_result = translate_log_entries(test_logs, target_language="fr")
    print(f"\nTranslated {entry_result['translated_count']} log entries to French")

    # Test support batch translation
    support_result = batch_translate_for_support(test_logs, support_locale="de")
    print(
        f"\nSupport translation to German: {support_result['translation_success_rate']}% success rate"
    )
    print(
        f"Created {len(support_result['support_ready_entries'])} support-ready entries"
    )
