"""Translate user-facing document fields using DeepL API.

Provider: DeepL API (deepl SDK)
Auth env: DEEPL_AUTH_KEY
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

import deepl

from database_models import DocumentResponse


_DEEPL_DEFAULT_TARGET = "EN"


def _extract_user_fields(record: DocumentResponse, field_names: Optional[List[str]] = None) -> Dict[str, str]:
    """Return a mapping of field name -> text value for translation."""
    if field_names is None:
        field_names = ["title", "description", "comment", "content", "summary"]
    result: Dict[str, str] = {}
    for fname in field_names:
        value = record.data.get(fname)
        if isinstance(value, str) and value.strip():
            result[fname] = value
    return result


def translate_records(
    records: List[DocumentResponse],
    target_lang: str = _DEEPL_DEFAULT_TARGET,
    source_lang: Optional[str] = None,
    field_names: Optional[List[str]] = None,
    auth_key: Optional[str] = None,
) -> List[DocumentResponse]:
    """Translate designated user-facing fields of each record via DeepL.

    Returns new DocumentResponse objects with translated field values.
    """
    key = auth_key or os.environ.get("DEEPL_AUTH_KEY", "")
    if not key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is not set")

    translator = deepl.Translator(key)

    translated: List[DocumentResponse] = []

    for record in records:
        fields_to_translate = _extract_user_fields(record, field_names)
        new_data = dict(record.data)

        if fields_to_translate:
            texts = list(fields_to_translate.values())
            deepl_results = translator.translate_text(
                texts,
                target_lang=target_lang,
                source_lang=source_lang,
            )
            for (field_name, _), deepl_result in zip(fields_to_translate.items(), deepl_results):
                new_data[field_name] = deepl_result.text

        translated.append(
            DocumentResponse(
                doc_id=record.doc_id,
                data=new_data,
                version=record.version,
                found=record.found,
            )
        )

    return translated


if __name__ == "__main__":
    sample = [
        DocumentResponse(doc_id="doc-1", data={"title": "Informe final", "description": "Resultado del proyecto."}, version=1, found=True),
    ]
    result = translate_records(sample, target_lang="EN")
    for r in result:
        print(f"{r.doc_id}: {r.data}")
