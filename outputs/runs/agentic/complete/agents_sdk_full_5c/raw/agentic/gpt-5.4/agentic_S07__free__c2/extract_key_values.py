from __future__ import annotations

from typing import List

from document_client import process_document
from document_models import KeyValueField, get_text


def extract_key_values(file_path: str) -> List[KeyValueField]:
    document = process_document(file_path)
    full_text = document.text or ""
    fields: List[KeyValueField] = []

    for entity in document.entities:
        mention_text = entity.mention_text or get_text(entity.text_anchor, full_text)
        fields.append(
            KeyValueField(
                key=entity.type_,
                value=mention_text,
                confidence=float(entity.confidence) if entity.confidence is not None else None,
                page=int(entity.page_anchor.page_refs[0].page) + 1 if entity.page_anchor and entity.page_anchor.page_refs else None,
            )
        )

        for prop in entity.properties:
            prop_text = prop.mention_text or get_text(prop.text_anchor, full_text)
            fields.append(
                KeyValueField(
                    key=f"{entity.type_}.{prop.type_}",
                    value=prop_text,
                    confidence=float(prop.confidence) if prop.confidence is not None else None,
                    page=int(prop.page_anchor.page_refs[0].page) + 1 if prop.page_anchor and prop.page_anchor.page_refs else None,
                )
            )

    return fields
