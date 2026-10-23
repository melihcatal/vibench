from typing import List, Dict, Any
from observability_client import get_google_translate_client
from observability_models import TranslationResult


def translate_log_messages(
    log_messages: List[Dict[str, Any]],
    target_language: str = "en",
    source_language: str = "auto",
) -> List[TranslationResult]:
    """
    Translate support-visible log messages for another locale using Google Cloud Translation.

    Args:
        log_messages: List of log messages with 'id' and 'message' fields
        target_language: Target language code (e.g., 'en', 'es', 'fr')
        source_language: Source language code or 'auto' for auto-detection

    Returns:
        List of translation results
    """
    results = []

    try:
        client = get_google_translate_client()

        # Extract messages for batch translation
        messages_to_translate = []
        message_indices = []

        for i, log in enumerate(log_messages):
            message = log.get("message", "")
            if message and len(message.strip()) > 0:
                messages_to_translate.append(message)
                message_indices.append(i)

        if not messages_to_translate:
            return []

        # Perform batch translation
        translations = client.translate(
            messages_to_translate,
            target_language=target_language,
            source_language=source_language,
        )

        # Map translations back to original logs
        translation_map = {}
        for idx, translation in zip(message_indices, translations):
            translation_map[idx] = translation

        # Create results
        for i, log in enumerate(log_messages):
            log_id = log.get("id", f"log-{i}")
            original_message = log.get("message", "")

            if i in translation_map:
                translation = translation_map[i]
                results.append(
                    TranslationResult(
                        original_text=original_message,
                        translated_text=translation["translatedText"],
                        source_language=translation.get(
                            "detectedSourceLanguage", source_language
                        ),
                        target_language=target_language,
                        provider="google",
                    )
                )
            else:
                # No translation needed or possible
                results.append(
                    TranslationResult(
                        original_text=original_message,
                        translated_text=original_message,
                        source_language=source_language,
                        target_language=target_language,
                        provider="none",
                    )
                )

    except Exception as e:
        # Fallback: return original messages
        for i, log in enumerate(log_messages):
            log_id = log.get("id", f"log-{i}")
            original_message = log.get("message", "")

            results.append(
                TranslationResult(
                    original_text=original_message,
                    translated_text=original_message,
                    source_language=source_language,
                    target_language=target_language,
                    provider="fallback",
                )
            )

    return results


def translate_single_log_message(
    message: str, target_language: str = "en", source_language: str = "auto"
) -> TranslationResult:
    """
    Translate a single log message.

    Args:
        message: Log message text
        target_language: Target language code
        source_language: Source language code

    Returns:
        Translation result
    """
    results = translate_log_messages(
        [{"id": "single", "message": message}],
        target_language=target_language,
        source_language=source_language,
    )
    return results[0] if results else None


def translate_for_support_team(
    log_messages: List[Dict[str, Any]], support_language: str = "en"
) -> Dict[str, Any]:
    """
    Translate logs for support team review.

    Args:
        log_messages: List of log messages
        support_language: Language code for support team

    Returns:
        Dictionary with translated logs and statistics
    """
    translation_results = translate_log_messages(
        log_messages, target_language=support_language
    )

    # Group by source language
    language_stats = {}
    for result in translation_results:
        source_lang = result.source_language
        language_stats[source_lang] = language_stats.get(source_lang, 0) + 1

    # Prepare translated logs
    translated_logs = []
    for log, result in zip(log_messages, translation_results):
        translated_logs.append(
            {
                "original_log": log,
                "translated_message": result.translated_text,
                "source_language": result.source_language,
                "target_language": result.target_language,
                "needed_translation": result.original_text != result.translated_text,
            }
        )

    # Calculate translation statistics
    total_logs = len(log_messages)
    translated_count = sum(
        1 for r in translation_results if r.original_text != r.translated_text
    )

    return {
        "translated_logs": translated_logs,
        "statistics": {
            "total_logs": total_logs,
            "translated_logs": translated_count,
            "translation_rate": translated_count / total_logs if total_logs > 0 else 0,
            "source_languages": language_stats,
            "target_language": support_language,
        },
        "provider": translation_results[0].provider
        if translation_results
        else "unknown",
    }


def detect_log_languages(log_messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Detect languages in log messages.

    Args:
        log_messages: List of log messages

    Returns:
        Language detection results
    """
    try:
        client = get_google_translate_client()

        # Extract messages for detection
        messages = []
        for log in log_messages:
            message = log.get("message", "")
            if message and len(message.strip()) > 0:
                messages.append(message)

        if not messages:
            return {"detected_languages": {}, "sample_size": 0}

        # Detect languages
        detections = client.detect_language(messages)

        # Count languages
        language_counts = {}
        for detection in detections:
            lang = detection["language"]
            confidence = detection.get("confidence", 0)

            if lang not in language_counts:
                language_counts[lang] = {
                    "count": 0,
                    "total_confidence": 0,
                    "samples": [],
                }

            language_counts[lang]["count"] += 1
            language_counts[lang]["total_confidence"] += confidence

            # Keep some sample messages
            if len(language_counts[lang]["samples"]) < 3:
                language_counts[lang]["samples"].append(
                    messages[len(language_counts[lang]["samples"])]
                )

        # Calculate average confidence
        for lang in language_counts:
            language_counts[lang]["average_confidence"] = (
                language_counts[lang]["total_confidence"]
                / language_counts[lang]["count"]
            )

        return {
            "detected_languages": language_counts,
            "sample_size": len(messages),
            "provider": "google",
        }

    except Exception as e:
        return {
            "detected_languages": {},
            "sample_size": 0,
            "error": str(e),
            "provider": "error",
        }
