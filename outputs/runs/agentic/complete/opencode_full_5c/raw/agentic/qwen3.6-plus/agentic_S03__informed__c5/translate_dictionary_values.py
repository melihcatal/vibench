import os
from deepl import Translator
from translation_models import (
    DictionaryTranslationRequest,
    DictionaryTranslationResponse,
)
from translation_client import get_deepl_client, normalize_language_code


def translate_dictionary_values(
    request: DictionaryTranslationRequest,
) -> DictionaryTranslationResponse:
    client = get_deepl_client()
    source_lang = normalize_language_code(request.source_lang)
    target_lang = normalize_language_code(request.target_lang)

    keys = list(request.dictionary.keys())
    values = list(request.dictionary.values())

    str_values = [str(v) for v in values]

    if not str_values:
        return DictionaryTranslationResponse(
            translated_dictionary={},
            source_lang=request.source_lang,
            target_lang=target_lang,
        )

    results = client.translate_text(
        str_values,
        source_lang=source_lang if source_lang else None,
        target_lang=target_lang,
    )

    translated_dict = {}
    for idx, key in enumerate(keys):
        translated_dict[key] = results[idx].text

    return DictionaryTranslationResponse(
        translated_dictionary=translated_dict,
        source_lang=request.source_lang,
        target_lang=target_lang,
    )


if __name__ == "__main__":
    req = DictionaryTranslationRequest(
        dictionary={
            "greeting": "Hello",
            "farewell": "Goodbye",
            "thanks": "Thank you",
        },
        source_lang="en",
        target_lang="ja",
    )
    resp = translate_dictionary_values(req)
    print(resp.translated_dictionary)
