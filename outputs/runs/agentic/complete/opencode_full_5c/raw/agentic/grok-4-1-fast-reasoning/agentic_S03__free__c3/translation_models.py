from typing import Union, Optional
import re


def normalize_language_code(lang_code: str) -> str:
    """
    Normalize language code to DeepL format (e.g., 'en' -> 'EN', 'en-US' -> 'EN-US').
    """
    lang_code = lang_code.strip().upper()
    # DeepL uses specific formats
    if lang_code == "EN-GB":
        return "EN-GB"
    # Add more mappings as needed
    return lang_code


def sanitize_text_for_translation(text: str) -> str:
    """
    Normalize text by trimming and normalizing whitespace.
    """
    return re.sub(r"\s+", " ", text.strip())


def extract_detected_lang(result: "deepl.Translation") -> str:
    """
    Extract detected source language from DeepL result.
    """
    return result.detected_source_lang
