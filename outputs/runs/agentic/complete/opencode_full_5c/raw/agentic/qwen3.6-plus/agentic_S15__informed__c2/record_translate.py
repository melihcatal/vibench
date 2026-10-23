from __future__ import annotations

import os
from typing import Any

import deepl
from database_models import DocumentResponse

DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")
DEFAULT_TARGET_LANG = "en"


def translate_documents(
    documents: list[DocumentResponse],
    target_lang: str = DEFAULT_TARGET_LANG,
    text_fields: list[str] | None = None,
) -> list[DocumentResponse]:
    if text_fields is None:
        text_fields = ["content", "text", "title", "description"]

    translator = deepl.Translator(DEEPL_AUTH_KEY)

    translated_docs = []

    for doc in documents:
        new_data = dict(doc.data)

        for field_name in text_fields:
            if field_name in new_data and isinstance(new_data[field_name], str):
                result = translator.translate_text(
                    new_data[field_name],
                    target_lang=target_lang,
                )
                new_data[f"{field_name}_translated"] = result.text
                new_data[f"{field_name}_source_lang"] = result.detected_source_lang

        translated_doc = DocumentResponse(
            document_id=doc.document_id,
            data=new_data,
            partition_key=doc.partition_key,
            version=doc.version,
            found=doc.found,
            updated_at=doc.updated_at,
        )
        translated_docs.append(translated_doc)

    return translated_docs
