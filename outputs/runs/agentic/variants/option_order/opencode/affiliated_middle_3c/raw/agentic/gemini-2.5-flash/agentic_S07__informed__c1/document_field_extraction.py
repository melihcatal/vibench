import os
from google.cloud import documentai_v1beta3 as documentai
from document_client import DocumentAIClient
from document_models import DocumentField
from typing import List


def extract_fields_from_document_ai_processor(
    project_id: str,
    location: str,
    processor_id: str,
    file_content: bytes,
    mime_type: str,
) -> List[DocumentField]:
    client = DocumentAIClient().client
    name = client.processor_path(project_id, location, processor_id)

    document = documentai.RawDocument(content=file_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=document)

    result = client.process_document(request=request)
    document_response = result.document

    extracted_fields: List[DocumentField] = []

    for entity in document_response.entities:
        field_name = entity.type_
        field_value = (
            entity.mention_text
            if entity.mention_text
            else entity.normalized_value.text
            if entity.normalized_value
            else ""
        )
        confidence = entity.confidence
        extracted_fields.append(
            DocumentField(
                field_name=field_name, field_value=field_value, confidence=confidence
            )
        )
    return extracted_fields
