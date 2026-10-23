import os
from typing import Dict, List, Any
from translation_client import TranslationClient


def quality_summary(
    original_text: str,
    translated_text: str,
    source_lang: str = "en",
    target_lang: str = "es",
) -> Dict[str, Any]:
    """
    Summarize translation quality issues using Google Cloud Translation API's quality estimation.

    Args:
        original_text: Original source text
        translated_text: Translated text
        source_lang: Source language code
        target_lang: Target language code

    Returns:
        Dictionary with quality metrics and issues
    """
    client = TranslationClient()

    # Use Google Cloud Translation API for quality assessment
    # Note: Google Cloud Translation doesn't have direct quality estimation API,
    # so we'll use alternative approaches

    # Approach 1: Back-translation to check consistency
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    # Back-translate to source language
    back_translation_result = translate_client.translate(
        translated_text, source_language=target_lang, target_language=source_lang
    )

    back_translated = back_translation_result["translatedText"]

    # Calculate basic metrics
    original_words = len(original_text.split())
    translated_words = len(translated_text.split())

    # Simple similarity check (in production, use more sophisticated methods)
    from difflib import SequenceMatcher

    similarity = SequenceMatcher(
        None, original_text.lower(), back_translated.lower()
    ).ratio()

    # Check for common issues
    issues = []

    # Length ratio check
    length_ratio = translated_words / max(original_words, 1)
    if length_ratio < 0.5:
        issues.append("translation_too_short")
    elif length_ratio > 2.0:
        issues.append("translation_too_long")

    # Back-translation similarity check
    if similarity < 0.7:
        issues.append("low_semantic_preservation")

    # Check for untranslated segments
    if any(word in translated_text for word in original_text.split()[:3]):
        issues.append("possible_untranslated_segments")

    # Use Perspective API for additional quality checks
    # (This would require additional setup with Perspective API)

    return {
        "original_text": original_text,
        "translated_text": translated_text,
        "back_translated": back_translated,
        "back_translation_similarity": similarity,
        "word_count_original": original_words,
        "word_count_translated": translated_words,
        "length_ratio": length_ratio,
        "detected_issues": issues,
        "quality_score": similarity * 100,  # Simple quality score
        "provider": "google-translation-api",
    }
