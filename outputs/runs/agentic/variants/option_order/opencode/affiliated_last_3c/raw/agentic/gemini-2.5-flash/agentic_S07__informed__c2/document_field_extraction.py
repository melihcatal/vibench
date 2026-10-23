import os
from typing import Dict, Any, List
from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client, get_processor_name
from document_models import DocumentInput, DocumentOutput


def extract_structured_fields_from_document(
    document_input: DocumentInput, project_id: str, location: str, processor_id: str
) -> DocumentOutput:
    """Extracts structured fields from a document using Google Document AI's specialized processors (e.g., Invoice Parser).
    Requires a processor trained for specific field extraction or a pre-trained processor like 'Invoice Parser'.
    """
    client = get_documentai_client()
    processor_name = get_processor_name(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=document_input.content,
        mime_type=document_input.mime_type,
    )

    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=raw_document,
    )

    response = client.process_document(request=request)
    document = response.document

    extracted_fields: List[Dict[str, Any]] = []
    for entity in document.entities:
        field_value = None
        if (
            entity.normalized_value
            and entity.normalized_value.text_anchor.text_segments
        ):
            field_value = document.text[
                entity.normalized_value.text_anchor.text_segments[
                    0
                ].start_index : entity.normalized_value.text_anchor.text_segments[
                    0
                ].end_index
            ]
        elif entity.text_anchor.text_segments:
            field_value = document.text[
                entity.text_anchor.text_segments[
                    0
                ].start_index : entity.text_anchor.text_segments[0].end_index
            ]
        elif entity.mention_text:
            field_value = entity.mention_text

        extracted_fields.append(
            {
                "field_name": entity.type,
                "field_value": field_value,
                "confidence": entity.confidence,
            }
        )

    return DocumentOutput(text=document.text, entities=extracted_fields)
