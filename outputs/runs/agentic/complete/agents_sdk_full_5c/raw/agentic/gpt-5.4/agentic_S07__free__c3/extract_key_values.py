from __future__ import annotations

from typing import List

from document_client import build_processor_name, get_documentai_client, get_processor_id, guess_mime_type
from document_models import DocumentRequest, KeyValuePair, load_bytes, normalize_text
from google.cloud import documentai_v1 as documentai


def _anchor_text(document: documentai.Document, anchor: documentai.Document.TextAnchor) -> str:
    parts = []
    for segment in anchor.text_segments:
        parts.append(document.text[int(segment.start_index):int(segment.end_index)])
    return normalize_text("".join(parts))


def extract_key_values(request: DocumentRequest) -> List[KeyValuePair]:
    client = get_documentai_client()
    processor_name = build_processor_name(get_processor_id("DOCUMENTAI_FORM_PARSER_PROCESSOR_ID"))
    raw_document = documentai.RawDocument(
        content=load_bytes(request.file_path),
        mime_type=guess_mime_type(request.file_path, request.mime_type),
    )
    result = client.process_document(
        request=documentai.ProcessRequest(name=processor_name, raw_document=raw_document)
    )
    pairs: List[KeyValuePair] = []
    for entity in result.document.entities:
        mention = normalize_text(entity.mention_text)
        key_name = entity.type_.replace("/", "_")
        normalized = entity.normalized_value.text if entity.normalized_value.text else mention
        pairs.append(
            KeyValuePair(
                key=key_name,
                value=normalized,
                confidence=entity.confidence,
            )
        )
        for prop in entity.properties:
            pairs.append(
                KeyValuePair(
                    key=f"{key_name}_{prop.type_.replace('/', '_')}",
                    value=_anchor_text(result.document, prop.text_anchor) or normalize_text(prop.mention_text),
                    confidence=prop.confidence,
                )
            )
    return pairs
