import os
from google.cloud import translate_v2 as translate
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class TranslationResult:
    """Result of translation operation."""

    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    confidence: Optional[float] = None


def translate_runbook_notes(
    text: str, target_language: str = "en", source_language: Optional[str] = None
) -> TranslationResult:
    """
    Translate secret-rotation runbook notes using Google Cloud Translation.

    Args:
        text: Text to translate
        target_language: Target language code (e.g., 'en', 'es', 'fr')
        source_language: Source language code (optional, auto-detected if not provided)

    Returns:
        TranslationResult with translation details
    """
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required"
        )

    client = translate.Client()

    try:
        if source_language:
            result = client.translate(
                text,
                target_language=target_language,
                source_language=source_language,
                format_="text",
            )
        else:
            result = client.translate(
                text, target_language=target_language, format_="text"
            )

        return TranslationResult(
            original_text=text,
            translated_text=result["translatedText"],
            source_language=result.get(
                "detectedSourceLanguage", source_language or "unknown"
            ),
            target_language=target_language,
            confidence=None,
        )

    except Exception as e:
        raise RuntimeError(f"Error translating text: {e}") from e


def translate_batch_runbook_notes(
    texts: List[str], target_language: str = "en", source_language: Optional[str] = None
) -> List[TranslationResult]:
    """
    Translate multiple runbook notes in batch.

    Args:
        texts: List of texts to translate
        target_language: Target language code
        source_language: Source language code (optional)

    Returns:
        List of TranslationResult objects
    """
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required"
        )

    client = translate.Client()

    try:
        if source_language:
            results = client.translate(
                texts,
                target_language=target_language,
                source_language=source_language,
                format_="text",
            )
        else:
            results = client.translate(
                texts, target_language=target_language, format_="text"
            )

        translation_results = []
        for i, result in enumerate(results):
            translation_results.append(
                TranslationResult(
                    original_text=texts[i],
                    translated_text=result["translatedText"],
                    source_language=result.get(
                        "detectedSourceLanguage", source_language or "unknown"
                    ),
                    target_language=target_language,
                    confidence=None,
                )
            )

        return translation_results

    except Exception as e:
        raise RuntimeError(f"Error translating batch texts: {e}") from e


def translate_runbook_sections(
    runbook: Dict[str, Any],
    target_language: str = "en",
    sections_to_translate: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Translate specific sections of a runbook.

    Args:
        runbook: Runbook dictionary
        target_language: Target language code
        sections_to_translate: List of section keys to translate (default: all text fields)

    Returns:
        Translated runbook dictionary
    """
    if sections_to_translate is None:
        sections_to_translate = [
            "title",
            "description",
            "steps",
            "notes",
            "troubleshooting",
        ]

    translated_runbook = runbook.copy()

    for section in sections_to_translate:
        if section in runbook:
            section_content = runbook[section]

            if isinstance(section_content, str):
                if section_content.strip():
                    result = translate_runbook_notes(section_content, target_language)
                    translated_runbook[section] = result.translated_text
            elif isinstance(section_content, list):
                translated_list = []
                for item in section_content:
                    if isinstance(item, str):
                        if item.strip():
                            result = translate_runbook_notes(item, target_language)
                            translated_list.append(result.translated_text)
                        else:
                            translated_list.append(item)
                    elif isinstance(item, dict):
                        translated_item = translate_runbook_sections(
                            item, target_language, ["text", "description", "title"]
                        )
                        translated_list.append(translated_item)
                    else:
                        translated_list.append(item)
                translated_runbook[section] = translated_list
            elif isinstance(section_content, dict):
                translated_runbook[section] = translate_runbook_sections(
                    section_content, target_language, ["text", "description", "title"]
                )

    translated_runbook["translation_metadata"] = {
        "target_language": target_language,
        "original_language": "auto-detected",
        "translated_sections": sections_to_translate,
    }

    return translated_runbook


def detect_runbook_language(text: str) -> str:
    """
    Detect the language of runbook text.

    Args:
        text: Text to analyze

    Returns:
        Language code
    """
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required"
        )

    client = translate.Client()

    try:
        result = client.detect_language(text)
        return result["language"]
    except Exception as e:
        raise RuntimeError(f"Error detecting language: {e}") from e
