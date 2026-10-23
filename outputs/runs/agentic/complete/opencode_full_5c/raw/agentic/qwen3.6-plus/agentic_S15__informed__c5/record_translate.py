import os
import deepl
from database_models import DocumentResponse


def translate_document_fields(
    document, target_lang, source_lang=None, text_fields=None
):
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)

    if isinstance(document, DocumentResponse):
        data = dict(document.data)
        doc_id = document.document_id
    elif isinstance(document, dict):
        data = dict(document)
        doc_id = document.get("document_id", document.get("id", "unknown"))
    else:
        raise ValueError("document must be a DocumentResponse or dict")

    if text_fields is None:
        text_fields = [k for k, v in data.items() if isinstance(v, str)]

    translate_kwargs = {}
    if source_lang:
        translate_kwargs["source_lang"] = source_lang

    translated_data = dict(data)
    translation_map = {}

    for field_name in text_fields:
        field_value = data.get(field_name, "")
        if not field_value or not field_value.strip():
            continue
        result = translator.translate_text(
            field_value, target_lang=target_lang, **translate_kwargs
        )
        translated_text = result.text
        translated_data[field_name] = translated_text
        translation_map[field_name] = {
            "original": field_value,
            "translated": translated_text,
            "detected_source_lang": result.detected_source_lang
            if hasattr(result, "detected_source_lang")
            else None,
        }

    return {
        "document_id": doc_id,
        "translated_data": translated_data,
        "target_language": target_lang,
        "translation_map": translation_map,
    }


def translate_documents(documents, target_lang, source_lang=None, text_fields=None):
    results = []
    for doc in documents:
        result = translate_document_fields(doc, target_lang, source_lang, text_fields)
        results.append(result)
    return results
