from document_client import get_document_processor_client
from document_models import KeyValuePair, ExtractedKeyValues
from google.cloud import documentai_v1 as documentai

def extract_key_values(project_id: str, location: str, processor_id: str, file_content: bytes, mime_type: str) -> ExtractedKeyValues:
    client = get_document_processor_client()

    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=file_content,
        mime_type=mime_type
    )

    request = documentai.ProcessRequest(
        name=name,
        raw_document=raw_document
    )

    result = client.process_document(request=request)
    document = result.document

    key_value_pairs = []
    for entity in document.entities:
        if entity.type == "form_field": # Assuming form fields are key-value pairs
            key = entity.mention_text
            value = entity.normalized_value.text if entity.normalized_value else entity.text_anchor.content
            key_value_pairs.append(KeyValuePair(key=key, value=value))
            
    return ExtractedKeyValues(key_value_pairs)
