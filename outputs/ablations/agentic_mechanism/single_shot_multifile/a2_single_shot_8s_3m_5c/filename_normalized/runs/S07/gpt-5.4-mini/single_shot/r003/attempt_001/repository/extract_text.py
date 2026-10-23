import base64
from google.cloud import documentai
from document_client import get_document_ai_client, get_processor_name, load_document_bytes, detect_mime_type, normalize_text_response


def extract_text(document_path: str, project_id: str = None, location: str = None, processor_id: str = None):
    client = get_document_ai_client()
    raw = load_document_bytes(document_path)
    mime_type = detect_mime_type(document_path)
    name = get_processor_name(project_id=project_id, location=location, processor_id=processor_id)
    request = documentai.ProcessRequest(
        name=name,
        raw_document=documentai.RawDocument(content=raw, mime_type=mime_type),
    )
    response = client.process_document(request=request)
    return normalize_text_response(response.document)
