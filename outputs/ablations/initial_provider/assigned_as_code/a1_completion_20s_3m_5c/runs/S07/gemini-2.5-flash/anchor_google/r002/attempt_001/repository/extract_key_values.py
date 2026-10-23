from typing import Dict, Any, List
from document_client import DocumentClient
from document_models import DocumentKeyValue
from google.cloud import documentai_v1 as documentai

def extract_key_values(payload: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    project_id = config["project_id"]
    location = config["location"]
    processor_id = config["processor_id"]

    client = DocumentClient(project_id, location)
    processor_path = client.get_document_processor_path(processor_id)

    raw_document = documentai.RawDocument(
        content=payload["document_bytes"], mime_type=payload["mime_type"]
    )

    request = documentai.ProcessRequest(
        name=processor_path,
        raw_document=raw_document
    )

    response = client.documentai_client.process_document(request=request)
    document = response.document

    extracted_key_values: List[DocumentKeyValue] = []

    for entity in document.entities:
        if entity.type == "form_field" and entity.properties:
            key = documentai.get_text_anchor_text(entity.text_anchor, document.text)
            value = ""
            if entity.properties[0].text_anchor.text_segments:
                 value = documentai.get_text_anchor_text(entity.properties[0].text_anchor, document.text)
            
            extracted_key_values.append(DocumentKeyValue(
                key=key,
                value=value,
                confidence=entity.confidence
            ))
        elif entity.type == "field" and entity.mention_text and entity.normalized_value.text:
            # This is a more generic way to extract key-value pairs if not specifically form_field
            key = entity.mention_text
            value = entity.normalized_value.text # Or use documentai.get_text_anchor_text(entity.text_anchor, document.text) for raw text
            extracted_key_values.append(DocumentKeyValue(
                key=key,
                value=value,
                confidence=entity.confidence
            ))

    return {"key_values": extracted_key_values}
