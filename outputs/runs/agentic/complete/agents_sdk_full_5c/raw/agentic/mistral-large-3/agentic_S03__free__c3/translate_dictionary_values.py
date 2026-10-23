from typing import Dict, List, Optional
from translation_client import get_translation_client
from batch_translate import batch_translate

def translate_dictionary_values(
    dictionary: Dict[str, str],
    source_lang: str,
    target_lang: str,
    model: str = "google-translate-v3",
    glossary_id: Optional[str] = None,
) -> Dict[str, str]:
    """Translate dictionary values while preserving keys using Google Cloud Translation API."""
    values = list(dictionary.values())
    translated_values = batch_translate(
        texts=values,
        source_lang=source_lang,
        target_lang=target_lang,
        model=model,
        glossary_id=glossary_id,
    )
    return {
        key: translated_values[i]
        for i, key in enumerate(dictionary.keys())
    }