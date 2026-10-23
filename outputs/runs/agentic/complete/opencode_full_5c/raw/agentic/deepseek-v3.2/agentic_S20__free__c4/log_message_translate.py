import os
from typing import List, Dict, Any, Optional
from deep_translator import GoogleTranslator
from googletrans import Translator as GoogleTransTranslator

from observability_models import LogEvent


def translate_log_message(
    log_text: str, target_lang: str = "es", source_lang: str = "auto"
) -> Dict[str, Any]:
    """
    Translate support-visible log messages for another locale using Google Translate.

    Args:
        log_text: The log message text to translate
        target_lang: Target language code (e.g., 'es' for Spanish, 'fr' for French)
        source_lang: Source language code ('auto' for auto-detection)

    Returns:
        Dictionary with translation results
    """
    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)

        translated_text = translator.translate(log_text)

        return {
            "success": True,
            "original_text": log_text,
            "translated_text": translated_text,
            "source_language": source_lang,
            "target_language": target_lang,
            "provider": "Google Translate API (deep-translator)",
        }

    except Exception as e:
        print(f"Error translating with Google Translate (deep-translator): {e}")

        try:
            translator = GoogleTransTranslator()
            result = translator.translate(log_text, dest=target_lang, src=source_lang)

            return {
                "success": True,
                "original_text": log_text,
                "translated_text": result.text,
                "source_language": result.src,
                "target_language": target_lang,
                "provider": "Google Translate (googletrans)",
            }

        except Exception as e2:
            print(f"Error with backup translator: {e2}")
            return {
                "success": False,
                "error": str(e2),
                "original_text": log_text,
                "target_language": target_lang,
                "provider": "Google Translate",
            }


def translate_logs(
    log_events: List[LogEvent], target_lang: str = "es"
) -> Dict[str, Any]:
    """
    Translate multiple log messages.

    Args:
        log_events: List of LogEvent objects
        target_lang: Target language code

    Returns:
        Dictionary with translation results for all logs
    """
    results = []
    successful = 0
    failed = 0

    for i, log_event in enumerate(log_events):
        print(f"Translating log {i + 1}/{len(log_events)} to {target_lang}...")

        result = translate_log_message(log_event.message, target_lang=target_lang)

        result["log_index"] = i
        result["log_level"] = (
            log_event.level.value
            if hasattr(log_event.level, "value")
            else str(log_event.level)
        )
        result["timestamp"] = (
            log_event.timestamp.isoformat() if log_event.timestamp else None
        )
        result["correlation_id"] = log_event.correlation_id

        results.append(result)

        if result.get("success", False):
            successful += 1
        else:
            failed += 1

    return {
        "total_logs": len(log_events),
        "successful_translations": successful,
        "failed_translations": failed,
        "target_language": target_lang,
        "results": results,
        "provider": "Google Translate",
    }


def create_multilingual_log_summary(
    log_events: List[LogEvent], languages: List[str] = None
) -> Dict[str, Any]:
    """
    Create log summary translated to multiple languages.

    Args:
        log_events: List of LogEvent objects
        languages: List of target language codes

    Returns:
        Dictionary with multilingual summaries
    """
    if languages is None:
        languages = ["es", "fr", "de", "ja", "zh-cn"]

    summaries = {}

    error_logs = [
        log for log in log_events if log.level in ["ERROR", "CRITICAL", "FATAL"]
    ]
    warning_logs = [log for log in log_events if log.level == "WARNING"]
    info_logs = [log for log in log_events if log.level == "INFO"]

    for lang in languages:
        lang_summary = {
            "error_count": len(error_logs),
            "warning_count": len(warning_logs),
            "info_count": len(info_logs),
            "sample_translations": [],
        }

        sample_logs = []
        if error_logs:
            sample_logs.append(error_logs[0])
        if warning_logs:
            sample_logs.append(warning_logs[0])
        if info_logs:
            sample_logs.append(info_logs[0])

        for sample in sample_logs[:3]:
            translation = translate_log_message(sample.message, target_lang=lang)
            if translation.get("success", False):
                lang_summary["sample_translations"].append(
                    {
                        "original": sample.message[:100] + "..."
                        if len(sample.message) > 100
                        else sample.message,
                        "translated": translation["translated_text"][:100] + "..."
                        if len(translation["translated_text"]) > 100
                        else translation["translated_text"],
                        "level": sample.level.value
                        if hasattr(sample.level, "value")
                        else str(sample.level),
                    }
                )

        summaries[lang] = lang_summary

    return {
        "total_logs": len(log_events),
        "languages": languages,
        "summaries": summaries,
        "provider": "Google Translate",
    }


def detect_log_languages(log_events: List[LogEvent]) -> Dict[str, Any]:
    """
    Detect languages used in log messages.

    Args:
        log_events: List of LogEvent objects

    Returns:
        Dictionary with language detection results
    """
    try:
        translator = GoogleTransTranslator()

        language_counts = {}
        detection_results = []

        for i, log_event in enumerate(log_events[:50]):
            try:
                detection = translator.detect(log_event.message)

                lang_code = detection.lang if hasattr(detection, "lang") else "unknown"
                confidence = (
                    detection.confidence if hasattr(detection, "confidence") else 0
                )

                language_counts[lang_code] = language_counts.get(lang_code, 0) + 1

                detection_results.append(
                    {
                        "log_index": i,
                        "message_preview": log_event.message[:50] + "..."
                        if len(log_event.message) > 50
                        else log_event.message,
                        "detected_language": lang_code,
                        "confidence": confidence,
                        "level": log_event.level.value
                        if hasattr(log_event.level, "value")
                        else str(log_event.level),
                    }
                )

            except Exception as e:
                print(f"Error detecting language for log {i}: {e}")

        return {
            "total_logs_analyzed": len(detection_results),
            "language_distribution": language_counts,
            "primary_language": max(language_counts.items(), key=lambda x: x[1])[0]
            if language_counts
            else "unknown",
            "detection_samples": detection_results[:10],
            "provider": "Google Translate Language Detection",
        }

    except Exception as e:
        print(f"Error in language detection: {e}")
        return {"error": str(e), "provider": "Google Translate"}


def translate_incident_summary(
    summary_text: str, target_lang: str = "es"
) -> Dict[str, Any]:
    """
    Translate incident summary text for international support teams.

    Args:
        summary_text: Incident summary text
        target_lang: Target language code

    Returns:
        Dictionary with translation result
    """
    return translate_log_message(summary_text, target_lang=target_lang)
