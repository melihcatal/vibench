import os
from typing import Dict, Any, Optional, List
from translation_client import TranslationClient
from translation_models import (
    DictionaryTranslationRequest,
    DictionaryTranslationResponse,
    Formality,
)
from translation_models import (
    extract_text_from_dict_values,
    reconstruct_dict_with_translations,
)


def translate_dictionary_values(
    dictionary: Dict[str, Any],
    target_lang: str,
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
    preserve_formatting: bool = False,
    skip_keys: Optional[List[str]] = None,
) -> Dict[str, Any]:
    client = TranslationClient()

    text_dict = extract_text_from_dict_values(dictionary, skip_keys)

    if not text_dict:
        return dictionary.copy()

    texts_to_translate = list(text_dict.values())

    formality_enum = None
    if formality:
        try:
            formality_enum = Formality(formality)
        except ValueError:
            formality_enum = None

    translated_texts = client.translate_batch(
        texts=texts_to_translate,
        target_lang=target_lang,
        source_lang=source_lang,
        formality=formality_enum.value if formality_enum else None,
        preserve_formatting=preserve_formatting,
    )

    translated_dict = {}
    keys = list(text_dict.keys())
    for i, key in enumerate(keys):
        translated_dict[key] = translated_texts[i]

    result = reconstruct_dict_with_translations(dictionary, translated_dict, skip_keys)

    return result


def translate_dictionary_with_request(
    request: DictionaryTranslationRequest,
) -> DictionaryTranslationResponse:
    client = TranslationClient()

    text_dict = extract_text_from_dict_values(request.dictionary, request.skip_keys)

    if not text_dict:
        return DictionaryTranslationResponse(
            translated_dictionary=request.dictionary.copy(),
            detected_source_language=None,
            character_count=0,
        )

    texts_to_translate = list(text_dict.values())

    translated_texts = client.translate_batch(
        texts=texts_to_translate,
        target_lang=request.target_lang,
        source_lang=request.source_lang,
        formality=request.formality.value if request.formality else None,
        preserve_formatting=request.preserve_formatting,
    )

    translated_dict = {}
    keys = list(text_dict.keys())
    for i, key in enumerate(keys):
        translated_dict[key] = translated_texts[i]

    result_dict = reconstruct_dict_with_translations(
        request.dictionary, translated_dict, request.skip_keys
    )

    total_chars = sum(len(text) for text in texts_to_translate)

    return DictionaryTranslationResponse(
        translated_dictionary=result_dict,
        detected_source_language=None,
        character_count=total_chars,
    )


if __name__ == "__main__":
    sample_dict = {
        "title": "Welcome to our website",
        "description": "This is a sample description text.",
        "button_text": "Click here",
        "footer": "Copyright 2023",
        "count": 42,
        "enabled": True,
    }

    translated = translate_dictionary_values(
        dictionary=sample_dict,
        target_lang="ES",
        source_lang="EN",
        skip_keys=["count", "enabled"],
    )

    print("Translated dictionary:")
    for key, value in translated.items():
        print(f"  {key}: {value}")
