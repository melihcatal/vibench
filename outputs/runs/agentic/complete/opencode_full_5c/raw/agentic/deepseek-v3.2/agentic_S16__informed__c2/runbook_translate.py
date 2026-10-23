import os
import deepl
from typing import List, Dict, Any, Optional


def translate_runbook_notes(text: str, target_lang: str = "EN") -> str:
    """
    Translate secret-rotation runbook notes using DeepL API.

    Args:
        text: Text to translate
        target_lang: Target language code (e.g., "EN", "ES", "FR", "DE", "JA")

    Returns:
        Translated text
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(text, target_lang=target_lang)

        return result.text

    except deepl.DeepLException as e:
        raise RuntimeError(f"DeepL API error: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Error translating text: {e}") from e


def translate_runbook_sections(
    runbook_sections: Dict[str, str], target_lang: str = "EN"
) -> Dict[str, str]:
    """
    Translate multiple runbook sections.

    Args:
        runbook_sections: Dictionary mapping section names to content
        target_lang: Target language code

    Returns:
        Dictionary of translated sections
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    translated_sections = {}

    for section_name, content in runbook_sections.items():
        try:
            result = translator.translate_text(content, target_lang=target_lang)
            translated_sections[section_name] = result.text
        except deepl.DeepLException as e:
            print(f"Warning: Failed to translate section '{section_name}': {e}")
            translated_sections[section_name] = content  # Keep original on error

    return translated_sections


def detect_runbook_language(text: str) -> Dict[str, Any]:
    """
    Detect the language of runbook notes using DeepL.

    Args:
        text: Text to analyze

    Returns:
        Language detection results
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    try:
        # DeepL doesn't have a direct language detection API in the Python SDK,
        # but we can try to translate to English and see what happens
        # or use a workaround by attempting translation

        # First, let's try to get usage information which might include language detection
        usage = translator.get_usage()

        # For actual language detection, we'll use a different approach
        # Try translating a small sample and see if it changes
        if len(text) > 50:
            sample = text[:50]
        else:
            sample = text

        try:
            # Try to translate to English
            result = translator.translate_text(sample, target_lang="EN")

            # Check if translation happened (text changed)
            # This is a heuristic - not perfect but works for most cases
            if result.text.lower() != sample.lower():
                detected_lang = "Non-English (likely requires translation)"
            else:
                detected_lang = "English (or very similar)"

            return {
                "detected_language": detected_lang,
                "confidence": "medium",  # Heuristic confidence
                "sample_text": sample,
                "translated_sample": result.text,
                "character_count": len(text),
                "usage": {
                    "character_limit": usage.character.limit
                    if usage.character
                    else None,
                    "character_count": usage.character.count
                    if usage.character
                    else None,
                },
            }

        except deepl.DeepLException as e:
            # If translation fails, it might be due to language issues
            return {
                "detected_language": "Unknown (translation failed)",
                "confidence": "low",
                "error": str(e),
                "sample_text": sample,
                "character_count": len(text),
            }

    except deepl.DeepLException as e:
        raise RuntimeError(f"DeepL API error: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Error detecting language: {e}") from e


def create_multilingual_runbook(
    runbook_content: Dict[str, str], target_languages: List[str]
) -> Dict[str, Dict[str, str]]:
    """
    Create a multilingual runbook by translating to multiple languages.

    Args:
        runbook_content: Original runbook content (dictionary of sections)
        target_languages: List of target language codes

    Returns:
        Nested dictionary: language -> section -> translated content
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    multilingual_runbook = {}

    for lang in target_languages:
        print(f"Translating to {lang}...")

        translated_sections = {}
        for section_name, content in runbook_content.items():
            try:
                result = translator.translate_text(content, target_lang=lang)
                translated_sections[section_name] = result.text
            except deepl.DeepLException as e:
                print(
                    f"Warning: Failed to translate section '{section_name}' to {lang}: {e}"
                )
                translated_sections[section_name] = f"[Translation failed: {e}]"

        multilingual_runbook[lang] = translated_sections

    return multilingual_runbook


def validate_translation_quality(
    original: str, translated: str, source_lang: str = "auto"
) -> Dict[str, Any]:
    """
    Validate translation quality by checking key security terms.

    Args:
        original: Original text
        translated: Translated text
        source_lang: Source language code (optional)

    Returns:
        Quality assessment results
    """
    # Key security terms that should be preserved
    security_terms = [
        "secret",
        "rotation",
        "password",
        "key",
        "token",
        "authentication",
        "authorization",
        "encryption",
        "access",
        "permission",
        "credential",
        "security",
        "audit",
        "compliance",
        "policy",
        "risk",
    ]

    # Check for presence of key terms in original
    original_lower = original.lower()
    translated_lower = translated.lower()

    missing_terms = []
    preserved_terms = []

    for term in security_terms:
        if term in original_lower:
            if term in translated_lower:
                preserved_terms.append(term)
            else:
                missing_terms.append(term)

    # Calculate preservation rate
    total_relevant_terms = len(preserved_terms) + len(missing_terms)
    if total_relevant_terms > 0:
        preservation_rate = len(preserved_terms) / total_relevant_terms
    else:
        preservation_rate = 1.0

    # Check length ratio (translation shouldn't be extremely different in length)
    length_ratio = len(translated) / len(original) if len(original) > 0 else 1.0

    # Quality assessment
    quality_score = 0.0
    quality_feedback = []

    if preservation_rate >= 0.9:
        quality_score += 0.4
        quality_feedback.append("Good preservation of security terms")
    elif preservation_rate >= 0.7:
        quality_score += 0.3
        quality_feedback.append("Moderate preservation of security terms")
    else:
        quality_feedback.append("Poor preservation of security terms")

    if 0.7 <= length_ratio <= 1.3:
        quality_score += 0.3
        quality_feedback.append("Appropriate translation length")
    else:
        quality_feedback.append(
            "Translation length significantly different from original"
        )

    # Check for common translation issues
    common_issues = []

    # Check for placeholder markers (indicating failed translation)
    if "[Translation failed" in translated:
        common_issues.append("Contains translation failure markers")
        quality_score -= 0.2

    # Check for HTML/XML tags (shouldn't be in plain text)
    if "<" in translated and ">" in translated:
        common_issues.append("Contains HTML/XML tags")
        quality_score -= 0.1

    # Normalize score to 0-1 range
    quality_score = max(0.0, min(1.0, quality_score))

    # Overall quality rating
    if quality_score >= 0.8:
        quality_rating = "Excellent"
    elif quality_score >= 0.6:
        quality_rating = "Good"
    elif quality_score >= 0.4:
        quality_rating = "Fair"
    else:
        quality_rating = "Poor"

    return {
        "quality_score": quality_score,
        "quality_rating": quality_rating,
        "preservation_rate": preservation_rate,
        "length_ratio": length_ratio,
        "preserved_terms": preserved_terms,
        "missing_terms": missing_terms,
        "total_relevant_terms": total_relevant_terms,
        "common_issues": common_issues,
        "feedback": quality_feedback,
        "original_length": len(original),
        "translated_length": len(translated),
    }
