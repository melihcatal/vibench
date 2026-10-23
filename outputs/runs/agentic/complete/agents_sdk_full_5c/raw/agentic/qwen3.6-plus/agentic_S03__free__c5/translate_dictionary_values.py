"""
Translate dictionary values while preserving keys using Google Cloud Translation API v3.
"""
from typing import Dict, List, Optional
from translation_client import create_default_client
from translation_models import DictionaryTranslationRequest


def translate_dictionary_values(
    data: Dict[str, str],
    target_language: str,
    source_language: str = None,
    translate_keys: bool = False,
    model: str = None,
) -> Dict[str, str]:
    """
    Translate dictionary values while preserving keys using Google Cloud Translation.
    
    Uses the Google Cloud Translation v3 API (translate.googleapis.com) to translate
    all string values in a dictionary. Keys are preserved by default. The Google NMT
    model handles the actual translation work.
    
    Args:
        data: Dictionary with string values to translate
        target_language: Target language code (e.g., 'es', 'ja')
        source_language: Source language code (optional, auto-detected if omitted)
        translate_keys: Whether to also translate dictionary keys (default False)
        model: Specific Google model to use
    
    Returns:
        New dictionary with translated values and original (or translated) keys
    """
    if not data:
        return {}

    request = DictionaryTranslationRequest(
        data=data,
        target_language=target_language,
        source_language=source_language,
        translate_keys=translate_keys,
    )

    client = create_default_client()

    items_to_translate: List[str] = []
    key_map: List[tuple] = []

    for key, value in data.items():
        if isinstance(value, str) and value.strip():
            items_to_translate.append(value)
            key_map.append((key, "value"))

    if request.translate_keys:
        for key in data.keys():
            if isinstance(key, str) and key.strip():
                items_to_translate.append(key)
                key_map.append((key, "key"))

    if not items_to_translate:
        return dict(data)

    batch_response = client.batch_translate(
        texts=items_to_translate,
        target_language=request.target_language,
        source_language=request.source_language,
        mime_type="text/plain",
        model=model,
    )

    translated_values = [t.translated_text for t in batch_response.translations]

    result = {}
    val_idx = 0
    key_idx = 0
    
    value_translations = {}
    key_translations = {}
    
    for idx, (original, item_type) in enumerate(key_map):
        if item_type == "value":
            value_translations[original] = translated_values[val_idx]
            val_idx += 1
        elif item_type == "key":
            key_translations[original] = translated_values[key_idx]
            key_idx += 1

    for original_key, original_value in data.items():
        if request.translate_keys:
            new_key = key_translations.get(original_key, original_key)
        else:
            new_key = original_key

        if isinstance(original_value, str) and original_value.strip():
            new_value = value_translations.get(original_value, original_value)
        else:
            new_value = original_value

        result[new_key] = new_value

    return result


if __name__ == "__main__":
    ui_strings = {
        "greeting": "Welcome to our app",
        "error_not_found": "Page not found",
        "button_submit": "Submit",
        "label_email": "Email address",
    }
    
    result = translate_dictionary_values(
        data=ui_strings,
        target_language="ja",
        source_language="en",
    )
    
    for key, value in result.items():
        print(f"  {key}: {value}")
