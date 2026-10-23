import base64
from google.cloud import documentai

from document_client import build_processor_name, get_document_ai_client, normalize_request
from document_models import DocumentRequest, OCRResponse, text_from_document


def extract_text(request: DocumentRequest) -> OCRResponse:
    request = normalize_request(request)
    client = get_document_ai_client()
    name = build_processor_name(request.project_id, request.location, request.processor_id)
    if request.content_b64:
        content = base64.b64decode(request.content_b64)
    else:
        content = request.content or b""
    raw_document = documentai.RawDocument(content=content, mime_type=request.mime_type)
    result = client.process_document(request={"name": name, "raw_document": raw_document})
    doc = result.document
    return OCRResponse(text=text_from_document(doc), pages=[{"page_number": p.page_number} for p in doc.pages], raw=doc)
