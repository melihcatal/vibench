from document_client import get_documentai_client, get_processor_path
from document_models import DocumentRequest, KeyValuePairExtractionResponse, KeyValuePair
from google.cloud.documentai_v1.types import RawDocument

def extract_key_values_from_document(
    document_request: DocumentRequest,
    project_id: str,
    location: str,
    processor_id: str,
) -> KeyValuePairExtractionResponse:
    """
    Extracts key-value pairs from a form-like document using Google Document AI (Form Parser).
    """
    client = get_documentai_client()
    processor_path = get_processor_path(project_id, location, processor_id)

    raw_document = RawDocument(content=document_request.content, mime_type=document_request.mime_type)
    
    request = {"name": processor_path, "raw_document": raw_document}
    result = client.process_document(request=request)
    
    document = result.document

    key_value_pairs = []
    for entity in document.entities:
        if entity.type == "form_field":
            key_text = document.text[entity.text_anchor.text_segments[0].start_index:entity.text_anchor.text_segments[0].end_index] if entity.text_anchor.text_segments else ""
            value_text = document.text[entity.properties[0].text_anchor.text_segments[0].start_index:entity.properties[0].text_anchor.text_segments[0].end_index] if entity.properties and entity.properties[0].text_anchor.text_segments else ""
            key_value_pairs.append(KeyValuePair(key=key_text.strip(), value=value_text.strip()))
            
    return KeyValuePairExtractionResponse(text_content=document.text, key_value_pairs=key_value_pairs)

