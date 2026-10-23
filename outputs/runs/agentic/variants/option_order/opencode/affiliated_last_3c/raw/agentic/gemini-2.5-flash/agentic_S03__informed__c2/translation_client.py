import os
from google.cloud import translate_v2 as translate
from typing import List, Dict

# Google Cloud Translation client initialization
translate_client = translate.Client()


def translate_text_content(
    text: str, target_language: str, source_language: str = None
) -> str:
    """Translates a single text string."""
    result = translate_client.translate(
        text, target_language=target_language, source_language=source_language
    )
    return result["translatedText"]


def batch_translate_text_content(
    texts: List[str], target_language: str, source_language: str = None
) -> List[str]:
    """Translates a list of text strings."""
    translated_texts = []
    for text in texts:
        translated_texts.append(
            translate_text_content(text, target_language, source_language)
        )
    return translated_texts


def translate_html_content(
    html: str, target_language: str, source_language: str = None
) -> str:
    """Translates HTML content while preserving tags."""
    result = translate_client.translate(
        html,
        target_language=target_language,
        source_language=source_language,
        format_="html",
    )
    return result["translatedText"]


def translate_dictionary_values_content(
    dictionary: Dict[str, str], target_language: str, source_language: str = None
) -> Dict[str, str]:
    """Translates values in a dictionary while preserving keys."""
    translated_dictionary = {}
    for key, value in dictionary.items():
        translated_dictionary[key] = translate_text_content(
            value, target_language, source_language
        )
    return translated_dictionary
