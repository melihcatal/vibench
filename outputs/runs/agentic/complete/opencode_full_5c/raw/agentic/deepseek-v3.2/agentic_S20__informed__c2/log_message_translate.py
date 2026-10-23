import os
from typing import List, Dict, Any, Optional
from google.cloud import translate_v2 as translate
from fetch_recent_logs import fetch_recent_logs


def translate_log_message(
    text: str, target_language: str = "es", source_language: str = None
) -> Dict[str, Any]:
    """
    Translate support-visible log messages for another locale using Google Cloud Translation.

    Args:
        text: Text to translate
        target_language: Target language code (e.g., 'es' for Spanish, 'fr' for French)
        source_language: Source language code (optional, auto-detected if None)

    Returns:
        Dictionary with translation results
    """
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set"
        )

    client = translate.Client()

    try:
        if source_language:
            result = client.translate(
                text, target_language=target_language, source_language=source_language
            )
        else:
            result = client.translate(text, target_language=target_language)

        translation_result = {
            "original_text": text,
            "translated_text": result["translatedText"],
            "target_language": target_language,
            "detected_source_language": result.get(
                "detectedSourceLanguage", source_language
            ),
            "api_used": "Google Cloud Translation API",
        }

        return translation_result

    except Exception as e:
        print(f"Error translating text with Google Cloud Translation: {e}")
        return {
            "original_text": text,
            "error": str(e),
            "api_used": "Google Cloud Translation API",
        }


def translate_recent_logs(
    target_language: str = "es",
    hours_back: int = 1,
    limit: int = 10,
    severity_filter: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Translate recent log messages for support visibility using Google Cloud Translation.

    Args:
        target_language: Target language code
        hours_back: Number of hours to look back
        limit: Maximum number of logs to translate
        severity_filter: Optional severity level to filter by

    Returns:
        List of translation results with context
    """
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set"
        )

    logs = fetch_recent_logs(
        hours_back=hours_back, limit=limit, severity=severity_filter
    )

    client = translate.Client()
    results = []

    for log in logs:
        if not log.message or len(log.message.strip()) < 3:
            continue

        try:
            translation = client.translate(log.message, target_language=target_language)

            result = {
                "original_message": log.message,
                "translated_message": translation["translatedText"],
                "target_language": target_language,
                "source_language": translation.get("detectedSourceLanguage", "auto"),
                "timestamp": log.timestamp.isoformat(),
                "severity": log.severity,
                "component": log.labels.get("component", "unknown"),
                "api_used": "Google Cloud Translation API",
            }

            results.append(result)

        except Exception as e:
            print(f"Error translating log message: {e}")

    print(
        f"Translated {len(results)} log messages to {target_language} using Google Cloud Translation"
    )
    return results


def batch_translate_logs(
    log_messages: List[str], target_language: str = "es", source_language: str = None
) -> Dict[str, Any]:
    """
    Batch translate multiple log messages using Google Cloud Translation.

    Args:
        log_messages: List of log messages to translate
        target_language: Target language code
        source_language: Source language code (optional)

    Returns:
        Dictionary with batch translation results
    """
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set"
        )

    client = translate.Client()

    translations = []
    failed_translations = []

    for i, message in enumerate(log_messages):
        if not message or len(message.strip()) < 3:
            continue

        try:
            if source_language:
                result = client.translate(
                    message,
                    target_language=target_language,
                    source_language=source_language,
                )
            else:
                result = client.translate(message, target_language=target_language)

            translations.append(
                {
                    "original": message,
                    "translated": result["translatedText"],
                    "source_language": result.get(
                        "detectedSourceLanguage", source_language
                    ),
                    "index": i,
                }
            )

        except Exception as e:
            failed_translations.append(
                {"message": message[:100], "error": str(e), "index": i}
            )

    summary = {
        "total_messages": len(log_messages),
        "successful_translations": len(translations),
        "failed_translations": len(failed_translations),
        "target_language": target_language,
        "source_language": source_language or "auto-detected",
        "api_used": "Google Cloud Translation API",
    }

    return {
        "summary": summary,
        "translations": translations[:50],
        "failed": failed_translations[:10],
    }


def translate_for_support_locales(
    log_message: str, support_locales: List[str] = None
) -> Dict[str, Any]:
    """
    Translate log message for multiple support locales using Google Cloud Translation.

    Args:
        log_message: Log message to translate
        support_locales: List of target language codes

    Returns:
        Dictionary with translations for all locales
    """
    if support_locales is None:
        support_locales = ["es", "fr", "de", "ja", "zh-CN", "pt"]

    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set"
        )

    client = translate.Client()

    translations = {}

    for locale in support_locales:
        try:
            result = client.translate(log_message, target_language=locale)
            translations[locale] = result["translatedText"]
        except Exception as e:
            translations[locale] = f"Translation error: {str(e)}"

    return {
        "original_message": log_message,
        "translations": translations,
        "locales_translated": support_locales,
        "api_used": "Google Cloud Translation API",
    }


if __name__ == "__main__":
    test_messages = [
        "Database connection failed: timeout after 30 seconds",
        "User authentication successful for user johndoe",
        "Warning: High memory usage detected (95%)",
        "Error processing payment transaction",
    ]

    for msg in test_messages:
        result = translate_log_message(msg, target_language="es")
        print(f"Original: {msg[:60]}...")
        print(f"Spanish: {result.get('translated_text', 'Error')[:60]}...")
        print()
