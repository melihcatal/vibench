import base64
from google.cloud import documentai

from document_client import build_processor_name, get_document_ai_client, normalize_request
from document_models import DocumentRequest, LayoutResponse


def extract_layout(request: DocumentRequest) -> LayoutResponse:
    request = normalize_request(request)
    client = get_document_ai_client()
    name = build_processor_name(request.project_id, request.location, request.processor_id)
    content = base64.b64decode(request.content_b64) if request.content_b64 else (request.content or b"")
    raw_document = documentai.RawDocument(content=content, mime_type=request.mime_type)
    result = client.process_document(request={"name": name, "raw_document": raw_document})
    doc = result.document
    blocks = []
    lines = []
    tables = []
    for page in doc.pages:
        for block in page.blocks:
            blocks.append({"page_number": page.page_number, "confidence": block.layout.confidence})
        for line in page.lines:
            lines.append({"page_number": page.page_number, "confidence": line.layout.confidence})
        for table in page.tables:
            tables.append({"page_number": page.page_number, "confidence": table.layout.confidence})
    return LayoutResponse(blocks=blocks, lines=lines, tables=tables, raw=doc)
