import os
import deepl
from database_models import DocumentResponse


DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY")


def translate_text(
    text: str, target_lang: str = "EN", source_lang: str | None = None
) -> str:
    translator = deepl.Translator(DEEPL_AUTH_KEY)
    kwargs = {}
    if source_lang:
        kwargs["source_lang"] = source_lang
    result = translator.translate_text(text, target_lang=target_lang, **kwargs)
    return result.text


def translate_document_fields(
    documents: list[DocumentResponse],
    target_lang: str = "EN",
    fields_to_translate: list[str] | None = None,
) -> list[DocumentResponse]:
    translated_docs = []
    for doc in documents:
        translated_data = dict(doc.data)
        for key, value in translated_data.items():
            if fields_to_translate and key not in fields_to_translate:
                continue
            if isinstance(value, str) and len(value) > 0:
                translated_data[key] = translate_text(value, target_lang=target_lang)
        translated_doc = DocumentResponse(
            document_id=doc.document_id,
            data=translated_data,
            collection=doc.collection,
            version=doc.version,
            metadata={**doc.metadata, "translated_to": target_lang},
        )
        translated_docs.append(translated_doc)
    return translated_docs
