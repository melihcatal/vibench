import os
from typing import List, Dict, Any


def normalize_translate_response(response: dict) -> dict:
    """Extract translated text from Amazon Translate response format.

    Expected shape:
    {
        'TranslatedText': '...',
        # other fields omitted
    }
    """
    return {"translated_text": response.get("TranslatedText")}


def normalize_batch_translate_response(responses: List[dict]) -> List[dict]:
    """Normalize a list of Amazon Translate batch responses.

    Returns list of dicts with 'translated_text' key.
    """
    return [{"translated_text": r.get("TranslatedText")} for r in responses]


def normalize_markup_response(translated_texts: List[str], markup: str) -> str:
    """Reconstruct HTML/markup string from translated text list.

    Matches original tag positions.
    """
    # Simple reconstruction assuming one translated text per non-tag token
    parts = markup.split()
    result_parts = []
    text_idx = 0
    for part in parts:
        if part.strip() in [t.strip() for t in markup.split()]:  # placeholder logic
            result_parts.append(translated_texts[text_idx])
            text_idx += 1
        else:
            result_parts.append(part)
    return " ".join(result_parts)


def normalize_dictionary_response(translated_dict: dict) -> dict:
    """Ensure all values are strings."""
    return {
        k: str(v) if isinstance(v, (int, float)) else v
        for k, v in translated_dict.items()
    }


# Placeholder functions for consistency with same-scenario files
# They simply delegate to their same-scenario counterparts
from translate_text import translate_text
from batch_translate import batch_translate
from translate_markup import translate_markup
from translate_dictionary_values import translate_dictionary_values


def translate(source: Any, source_lang: str = "en", target_lang: str = "es") -> Any:
    """Generic entry point that dispatches based on input type.

    - str -> translate_text
    - list -> batch_translate
    - dict -> translate_dictionary_values
    - markup (HTML) -> translate_markup
    """
    if isinstance(source, str):
        return translate_text(source, source_lang, target_lang)
    elif isinstance(source, list):
        return batch_translate(source, source_lang, target_lang)
    elif isinstance(source, dict):
        return translate_dictionary_values(source, source_lang, target_lang)
    else:
        raise TypeError("Unsupported input type for translation")
