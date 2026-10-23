from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client
from document_models import DocumentPayload, DocumentConfig, KeyValueExtractionResult


def extract_key_values(payload: DocumentPayload, config: DocumentConfig) -> KeyValueExtractionResult:
    client = get_documentai_client(config.location)
    name = client.processor_path(config.project_id, config.location, config.processor_id)
    
    raw_document = documentai.RawDocument(
        content=payload.document_bytes, mime_type=payload.mime_type
    )
    
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    response = client.process_document(request=request)
    
    document = response.document
    
    key_value_pairs = []
    for entity in document.entities:
        if entity.type == "form_field":  # Assuming form_field entities represent key-value pairs
            key_text = client.common.text_anchor_to_string(entity.text_anchor, document.text)
            value_text = ""
            if entity.page_anchor:
                # Attempt to get the value from the mention_text or from the first property of the entity
                if entity.mention_text: # Prefer mention_text if it's the value
                    value_text = entity.mention_text
                elif entity.properties: # Otherwise, check properties
                    for prop in entity.properties:
                        if prop.type == "value": # Assuming 'value' property holds the value
                            value_text = client.common.text_anchor_to_string(prop.text_anchor, document.text)
                            break

            key_value_pairs.append({
                "key": key_text,
                "value": value_text,
                "confidence": entity.confidence
            })

    return KeyValueExtractionResult(key_value_pairs=key_value_pairs)
