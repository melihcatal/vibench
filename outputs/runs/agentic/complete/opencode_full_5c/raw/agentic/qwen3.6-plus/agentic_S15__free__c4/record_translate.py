import os
import json
import deepl

DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")
DEEPL_API_URL = "https://api-free.deepl.com"


def translate_text(text: str, target_lang: str = "EN", source_lang: str = None) -> str:
    translator = deepl.Translator(DEEPL_AUTH_KEY, server_url=DEEPL_API_URL)

    kwargs = {"target_lang": target_lang}
    if source_lang:
        kwargs["source_lang"] = source_lang

    result = translator.translate_text(text, **kwargs)
    return result.text


def translate_document_fields(
    document: dict,
    target_lang: str = "EN",
    source_lang: str = None,
    fields_to_translate: list = None,
) -> dict:
    if hasattr(document, "to_dict"):
        doc_data = document.to_dict()
    else:
        doc_data = document

    data = doc_data.get("data", doc_data)
    if isinstance(data, str):
        data = json.loads(data)

    if fields_to_translate is None:
        fields_to_translate = [k for k, v in data.items() if isinstance(v, str)]

    translated_data = dict(data)

    for field in fields_to_translate:
        value = data.get(field, "")
        if value and isinstance(value, str) and len(value.strip()) > 0:
            translated_value = translate_text(value, target_lang, source_lang)
            translated_data[field] = translated_value
            translated_data[f"{field}_translated_from"] = source_lang or "auto"
            translated_data[f"{field}_translated_to"] = target_lang

    translated_doc = dict(doc_data)
    translated_doc["data"] = translated_data

    return translated_doc
