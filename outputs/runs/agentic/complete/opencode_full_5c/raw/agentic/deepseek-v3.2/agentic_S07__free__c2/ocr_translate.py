import os
from typing import List, Dict, Any, Optional
import requests


def translate_ocr_text(
    text: str, target_language: str = "en", source_language: Optional[str] = None
) -> str:
    """
    Translate extracted OCR text using Google Cloud Translation API.

    Args:
        text: Text to translate
        target_language: Target language code (e.g., 'en', 'es', 'fr')
        source_language: Optional source language code (auto-detected if not provided)

    Returns:
        Translated text
    """
    from google.cloud import translate_v2 as translate

    client = translate.Client()

    if source_language:
        result = client.translate(
            text, target_language=target_language, source_language=source_language
        )
    else:
        result = client.translate(text, target_language=target_language)

    return result["translatedText"]


def translate_batch_ocr_texts(
    texts: List[str], target_language: str = "en"
) -> List[str]:
    """
    Translate multiple OCR texts in batch using Google Cloud Translation API.

    Args:
        texts: List of texts to translate
        target_language: Target language code

    Returns:
        List of translated texts
    """
    from google.cloud import translate_v2 as translate

    client = translate.Client()

    results = client.translate(texts, target_language=target_language)

    return [result["translatedText"] for result in results]


def translate_with_detection(text: str, target_language: str = "en") -> Dict[str, Any]:
    """
    Translate text with language detection using Google Cloud Translation API.

    Args:
        text: Text to translate
        target_language: Target language code

    Returns:
        Dictionary with translation and detection results
    """
    from google.cloud import translate_v2 as translate

    client = translate.Client()

    result = client.translate(text, target_language=target_language, format_="text")

    return {
        "original_text": text,
        "translated_text": result["translatedText"],
        "detected_language": result["detectedSourceLanguage"],
        "target_language": target_language,
        "confidence": None,
    }


def translate_document_sections(
    sections: Dict[str, str], target_language: str = "en"
) -> Dict[str, str]:
    """
    Translate different sections of a document (headers, paragraphs, etc.).

    Args:
        sections: Dictionary mapping section names to text
        target_language: Target language code

    Returns:
        Dictionary with translated sections
    """
    from google.cloud import translate_v2 as translate

    client = translate.Client()

    translated_sections = {}

    for section_name, section_text in sections.items():
        if section_text.strip():
            result = client.translate(section_text, target_language=target_language)
            translated_sections[section_name] = result["translatedText"]
        else:
            translated_sections[section_name] = ""

    return translated_sections


def translate_with_preserved_formatting(text: str, target_language: str = "en") -> str:
    """
    Translate text while preserving basic formatting (newlines, spacing).

    Args:
        text: Text to translate
        target_language: Target language code

    Returns:
        Translated text with preserved formatting
    """
    from google.cloud import translate_v2 as translate

    client = translate.Client()

    paragraphs = text.split("\n\n")
    translated_paragraphs = []

    for paragraph in paragraphs:
        if paragraph.strip():
            lines = paragraph.split("\n")
            translated_lines = []

            for line in lines:
                if line.strip():
                    result = client.translate(line, target_language=target_language)
                    translated_lines.append(result["translatedText"])
                else:
                    translated_lines.append("")

            translated_paragraphs.append("\n".join(translated_lines))
        else:
            translated_paragraphs.append("")

    return "\n\n".join(translated_paragraphs)
