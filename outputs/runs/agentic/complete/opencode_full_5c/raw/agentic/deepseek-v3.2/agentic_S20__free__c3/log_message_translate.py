import json
from typing import Dict, Any, List, Optional
from deep_translator import GoogleTranslator
from fetch_recent_logs import fetch_recent_logs
from observability_models import LogEntry


def translate_log_message(
    text: str, target_language: str = "es", source_language: str = "auto"
) -> Dict[str, Any]:
    try:
        translator = GoogleTranslator(source=source_language, target=target_language)

        translated_text = translator.translate(text)

        return {
            "original_text": text,
            "translated_text": translated_text,
            "target_language": target_language,
            "source_language": source_language,
            "success": True,
            "character_count": len(text),
            "translation_provider": "Google Translate API",
        }
    except Exception as e:
        return {
            "original_text": text,
            "translated_text": None,
            "target_language": target_language,
            "error": str(e),
            "success": False,
            "translation_provider": "Google Translate API",
        }


def translate_log_entry(
    log_entry: LogEntry, target_language: str = "es"
) -> Dict[str, Any]:
    translation_result = translate_log_message(log_entry.message, target_language)

    translated_entry = {
        "original_entry": {
            "timestamp": log_entry.timestamp,
            "level": log_entry.level,
            "service": log_entry.service,
            "component": log_entry.component,
            "message": log_entry.message[:150] + "..."
            if len(log_entry.message) > 150
            else log_entry.message,
        },
        "translation": translation_result,
        "metadata": {
            "correlation_id": log_entry.correlation_id,
            "requires_translation": translation_result["success"],
        },
    }

    return translated_entry


def translate_recent_logs(
    minutes_ago: int = 30,
    target_language: str = "es",
    limit: int = 20,
    service_filter: Optional[str] = None,
) -> Dict[str, Any]:
    logs_response = fetch_recent_logs(
        minutes_ago=minutes_ago, service=service_filter, limit=limit
    )

    translated_logs = []
    failed_translations = 0

    for event in logs_response.events:
        try:
            log_data = json.loads(event.get("message", ""))
            log_message = log_data.get("message", "")

            if log_message:
                translation_result = translate_log_message(log_message, target_language)

                if translation_result["success"]:
                    translated_logs.append(
                        {
                            "timestamp": event.get("timestamp"),
                            "service": log_data.get("service", "unknown"),
                            "original_message": log_message[:100] + "..."
                            if len(log_message) > 100
                            else log_message,
                            "translated_message": translation_result["translated_text"][
                                :100
                            ]
                            + "..."
                            if translation_result["translated_text"]
                            and len(translation_result["translated_text"]) > 100
                            else translation_result["translated_text"],
                            "language": target_language,
                        }
                    )
                else:
                    failed_translations += 1
        except:
            failed_translations += 1
            continue

    return {
        "total_logs_processed": len(logs_response.events),
        "successfully_translated": len(translated_logs),
        "failed_translations": failed_translations,
        "target_language": target_language,
        "time_range": f"Last {minutes_ago} minutes",
        "translated_logs_sample": translated_logs[:5],
        "translation_provider": "Google Translate API",
    }


def batch_translate_logs(
    log_messages: List[str], target_language: str = "fr", batch_size: int = 10
) -> List[Dict[str, Any]]:
    results = []

    for i in range(0, len(log_messages), batch_size):
        batch = log_messages[i : i + batch_size]

        for message in batch:
            result = translate_log_message(message, target_language)
            results.append(result)

    return results


def translate_for_support_team(
    correlation_id: str, target_language: str = "es"
) -> Dict[str, Any]:
    from write_correlated_logs import generate_correlation_id

    logs_response = fetch_recent_logs(
        minutes_ago=120, correlation_id=correlation_id, limit=50
    )

    support_translations = []

    for event in logs_response.events:
        try:
            log_data = json.loads(event.get("message", ""))
            log_message = log_data.get("message", "")
            log_level = log_data.get("level", "INFO")

            if log_message and log_level in ["ERROR", "WARNING"]:
                translation_result = translate_log_message(log_message, target_language)

                if translation_result["success"]:
                    support_translations.append(
                        {
                            "correlation_id": correlation_id,
                            "timestamp": event.get("timestamp"),
                            "service": log_data.get("service", "unknown"),
                            "level": log_level,
                            "original_message": log_message,
                            "translated_message": translation_result["translated_text"],
                            "translation_language": target_language,
                            "for_support_team": True,
                        }
                    )
        except:
            continue

    return {
        "correlation_id": correlation_id,
        "total_error_warning_logs": len(support_translations),
        "target_language": target_language,
        "translations": support_translations,
        "summary": f"Translated {len(support_translations)} error/warning logs for support team in {target_language}",
    }


def get_supported_languages() -> List[Dict[str, str]]:
    supported_languages = [
        {"code": "es", "name": "Spanish", "native_name": "Español"},
        {"code": "fr", "name": "French", "native_name": "Français"},
        {"code": "de", "name": "German", "native_name": "Deutsch"},
        {"code": "it", "name": "Italian", "native_name": "Italiano"},
        {"code": "pt", "name": "Portuguese", "native_name": "Português"},
        {"code": "ru", "name": "Russian", "native_name": "Русский"},
        {"code": "zh-CN", "name": "Chinese (Simplified)", "native_name": "中文 (简体)"},
        {"code": "ja", "name": "Japanese", "native_name": "日本語"},
        {"code": "ko", "name": "Korean", "native_name": "한국어"},
        {"code": "ar", "name": "Arabic", "native_name": "العربية"},
    ]

    return supported_languages


if __name__ == "__main__":
    test_message = "Database connection failed: Connection timeout after 30 seconds"
    translation = translate_log_message(test_message, target_language="es")
    print(f"Translation result: {json.dumps(translation, indent=2)}")

    recent_translations = translate_recent_logs(
        minutes_ago=15, target_language="fr", limit=10
    )
    print(f"\nRecent logs translation: {json.dumps(recent_translations, indent=2)}")

    languages = get_supported_languages()
    print(f"\nSupported languages: {len(languages)} languages available")
