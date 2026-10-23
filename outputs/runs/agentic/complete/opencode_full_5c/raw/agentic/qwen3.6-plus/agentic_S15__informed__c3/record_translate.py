import os
import deepl
from database_models import FetchResponse


DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")
DEEPL_API_URL = "https://api-free.deepl.com"


def translate_text(
    text: str, target_lang: str = "EN", source_lang: str | None = None
) -> dict:
    if not text or not text.strip():
        return {
            "provider": "deepl",
            "original": text,
            "translated": "",
            "source_lang": source_lang or "auto",
            "target_lang": target_lang,
        }

    translator = deepl.Translator(DEEPL_AUTH_KEY, server_url=DEEPL_API_URL)

    translate_kwargs = {"target_lang": target_lang.upper()}
    if source_lang:
        translate_kwargs["source_lang"] = source_lang.upper()

    result = translator.translate_text(text, **translate_kwargs)

    return {
        "provider": "deepl",
        "original": text,
        "translated": result.text,
        "source_lang": result.source_lang,
        "target_lang": target_lang,
    }


def translate_document_fields(
    document_data: dict,
    target_lang: str = "EN",
    source_lang: str | None = None,
    fields_to_translate: list[str] | None = None,
) -> dict:
    if fields_to_translate is None:
        fields_to_translate = [
            "title",
            "content",
            "description",
            "body",
            "text",
            "comment",
            "summary",
        ]

    translations = {}
    translated_data = dict(document_data)

    for field_name in fields_to_translate:
        if field_name in document_data and document_data[field_name]:
            field_text = document_data[field_name]
            if isinstance(field_text, str) and field_text.strip():
                translation_result = translate_text(
                    field_text, target_lang, source_lang
                )
                translations[field_name] = translation_result
                translated_data[field_name] = translation_result["translated"]

    return {
        "provider": "deepl",
        "target_lang": target_lang,
        "source_lang": source_lang or "auto",
        "translations": translations,
        "translated_document": translated_data,
    }


def translate_fetch_response(
    fetch_response: FetchResponse,
    target_lang: str = "EN",
    source_lang: str | None = None,
) -> dict:
    if not fetch_response.found or not fetch_response.data:
        return {
            "provider": "deepl",
            "target_lang": target_lang,
            "source_lang": source_lang or "auto",
            "translations": {},
            "translated_document": None,
            "message": "No document data to translate",
        }
    return translate_document_fields(fetch_response.data, target_lang, source_lang)


if __name__ == "__main__":
    sample_doc = {
        "title": "Documento de ejemplo",
        "content": "Este es un documento en espa\u00f1ol que necesita ser traducido.",
        "status": "active",
    }
    result = translate_document_fields(sample_doc, target_lang="EN")
    print(result)
