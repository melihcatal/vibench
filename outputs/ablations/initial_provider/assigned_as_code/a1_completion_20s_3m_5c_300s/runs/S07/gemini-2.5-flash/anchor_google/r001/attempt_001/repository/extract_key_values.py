from google.cloud import documentai
from document_client import get_document_ai_client
from document_models import DocumentAIConfig, DocumentPayload

def extract_key_values(payload: DocumentPayload, config: DocumentAIConfig):
    client = get_document_ai_client(config.location)
    name = client.processor_path(config.project_id, config.location, config.processor_id)

    raw_document = documentai.RawDocument(content=payload.document_bytes, mime_type=payload.mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    response = client.process_document(request=request)

    extracted_key_values = []
    for entity in response.document.entities:
        if entity.type == "form_field":  # Assuming form_field entities contain key-value pairs
            key = entity.text_anchor.text_segments[0].start_index if entity.text_anchor.text_segments else ""
            value = entity.value_anchor.text_segments[0].start_index if entity.value_anchor.text_segments else ""
            extracted_key_values.append({"key": key, "value": value})

    return {"key_values": extracted_key_values}
