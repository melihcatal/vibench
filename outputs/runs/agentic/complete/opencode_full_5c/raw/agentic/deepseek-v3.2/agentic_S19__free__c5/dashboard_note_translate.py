import os
from typing import Dict, Any
from google.cloud import translate_v2 as translate


def translate_dashboard_notes(
    notes_text: str, target_language: str = "es"
) -> Dict[str, Any]:
    """Translate metric or dashboard notes for another locale using Google Cloud Translation API."""
    client = translate.Client()

    try:
        result = client.translate(
            notes_text, target_language=target_language, format_="text"
        )

        translation = {
            "original_text": notes_text,
            "translated_text": result["translatedText"],
            "target_language": target_language,
            "detected_language": result.get("detectedSourceLanguage", "en"),
            "character_count": len(notes_text),
            "translation_metadata": {
                "model": "google-translation-api",
                "provider": "Google Cloud Translation",
            },
        }

        return translation

    except Exception as e:
        return {
            "original_text": notes_text,
            "target_language": target_language,
            "error": str(e),
            "translation_available": False,
        }


def translate_metric_descriptions(
    descriptions: Dict[str, str], target_language: str = "fr"
) -> Dict[str, Any]:
    """Translate multiple metric descriptions at once."""
    client = translate.Client()

    translations = {}
    failed_translations = []

    for metric_name, description in descriptions.items():
        try:
            result = client.translate(
                description, target_language=target_language, format_="text"
            )

            translations[metric_name] = {
                "original": description,
                "translated": result["translatedText"],
                "detected_language": result.get("detectedSourceLanguage", "en"),
            }

        except Exception as e:
            failed_translations.append({"metric": metric_name, "error": str(e)})

    return {
        "target_language": target_language,
        "total_metrics": len(descriptions),
        "successful_translations": len(translations),
        "failed_translations": len(failed_translations),
        "translations": translations,
        "failures": failed_translations,
    }


def validate_translation_quality(original: str, translated: str) -> Dict[str, Any]:
    """Validate translation quality using basic heuristics."""

    quality_checks = {
        "length_ratio": len(translated) / len(original) if len(original) > 0 else 1.0,
        "has_placeholders": any(
            char in translated for char in ["{", "}", "[", "]", "<", ">"]
        ),
        "has_untranslated_words": False,
        "special_characters_preserved": True,
    }

    common_metric_terms = ["cpu", "memory", "disk", "network", "latency", "throughput"]
    untranslated_terms = []

    for term in common_metric_terms:
        if term in original.lower() and term in translated.lower():
            untranslated_terms.append(term)

    if untranslated_terms:
        quality_checks["has_untranslated_words"] = True
        quality_checks["untranslated_terms"] = untranslated_terms

    special_chars = ["%", "$", "€", "£", "¥", "°"]
    for char in special_chars:
        if char in original and char not in translated:
            quality_checks["special_characters_preserved"] = False
            break

    quality_score = 0.0
    if 0.5 <= quality_checks["length_ratio"] <= 2.0:
        quality_score += 0.4

    if not quality_checks["has_placeholders"]:
        quality_score += 0.3

    if quality_checks["special_characters_preserved"]:
        quality_score += 0.2

    if not quality_checks["has_untranslated_words"]:
        quality_score += 0.1

    quality_checks["quality_score"] = quality_score

    return quality_checks


def translate_with_quality_check(
    notes_text: str, target_language: str = "de"
) -> Dict[str, Any]:
    """Translate dashboard notes with quality validation."""
    translation_result = translate_dashboard_notes(notes_text, target_language)

    if "error" in translation_result:
        return translation_result

    quality_check = validate_translation_quality(
        translation_result["original_text"], translation_result["translated_text"]
    )

    translation_result["quality_assessment"] = quality_check

    if quality_check["quality_score"] < 0.7:
        translation_result["recommendation"] = "Consider manual review of translation"
    else:
        translation_result["recommendation"] = "Translation appears acceptable"

    return translation_result
