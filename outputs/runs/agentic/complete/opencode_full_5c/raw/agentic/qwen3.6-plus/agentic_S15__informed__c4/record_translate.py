import os
from typing import Any, Dict, List, Optional

import deepl

from database_models import DocumentResponse


DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")
DEEPL_TARGET_LANG = os.environ.get("DEEPL_TARGET_LANG", "EN")


def translate_documents(
    documents: List[Dict[str, Any]],
    target_lang: Optional[str] = None,
    source_lang: Optional[str] = None,
    text_fields: Optional[List[str]] = None,
) -> DocumentResponse:
    if not documents:
        return DocumentResponse(
            success=False,
            error="No documents provided for translation",
        )

    if not DEEPL_AUTH_KEY:
        return DocumentResponse(
            success=False,
            error="DEEPL_AUTH_KEY environment variable is not set",
        )

    target_lang = target_lang or DEEPL_TARGET_LANG
    text_fields = text_fields or [
        "title",
        "content",
        "description",
        "body",
        "text",
        "message",
        "summary",
    ]

    translator = deepl.Translator(DEEPL_AUTH_KEY)

    translated_documents = []

    for doc in documents:
        doc_id = doc.get("id", doc.get("_id", "unknown"))
        translated_doc = dict(doc)
        translations_applied = []

        for field in text_fields:
            if field in translated_doc and isinstance(translated_doc[field], str):
                original_text = translated_doc[field]
                if not original_text.strip():
                    continue

                try:
                    result = translator.translate_text(
                        original_text,
                        source_lang=source_lang,
                        target_lang=target_lang,
                    )
                    translated_doc[field] = result.text
                    translations_applied.append(field)
                except deepl.DeepLException as exc:
                    translated_doc[f"{field}_translation_error"] = str(exc)

        translated_documents.append(
            {
                "document_id": doc_id,
                "document": translated_doc,
                "fields_translated": translations_applied,
                "target_language": target_lang,
            }
        )

    return DocumentResponse(
        success=True,
        document={
            "total_documents": len(documents),
            "target_language": target_lang,
            "source_language": source_lang or "auto-detect",
            "translated_documents": translated_documents,
            "service": "DeepL API",
        },
    )
