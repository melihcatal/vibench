import base64
from google.cloud import documentai

from document_client import build_processor_name, get_document_ai_client, normalize_request
from document_models import DocumentRequest, KeyValueResponse, kv_pairs_from_document


def extract_key_values(request: DocumentRequest) -> KeyValueResponse:
    request = normalize_request(request)
    client = get_document_ai_client()
    name = build_processor_name(request.project_id, request.location, request.processor_id)
    content = base64.b64decode(request.content_b64) if request.content_b64 else (request.content or b"")
    raw_document = documentai.RawDocument(content=content, mime_type=request.mime_type)
    result = client.process_document(request={"name": name, "raw_document": raw_document})
    doc = result.document
    return KeyValueResponse(pairs=kv_pairs_from_document(doc), raw=doc)
