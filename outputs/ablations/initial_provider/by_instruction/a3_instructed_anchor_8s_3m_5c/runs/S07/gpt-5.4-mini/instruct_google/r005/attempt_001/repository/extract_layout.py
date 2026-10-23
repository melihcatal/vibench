from google.cloud import documentai_v1 as documentai

from document_client import documentai_client, documentai_raw_document, get_env, processor_name
from document_models import LayoutResponse, OCRRequest, normalize_blocks


def extract_layout(request: OCRRequest) -> LayoutResponse:
    client = documentai_client()
    name = processor_name(get_env("GOOGLE_CLOUD_PROJECT", ""), get_env("GOOGLE_CLOUD_LOCATION", "us"), get_env("GOOGLE_CLOUD_DOCUMENTAI_LAYOUT_PROCESSOR_ID", ""))
    raw = documentai_raw_document(request.image_uri, request.image_bytes)
    result = client.process_document(name=name, raw_document=raw)
    document = result.document
    blocks = []
    for page in document.pages:
        for paragraph in page.paragraphs:
            blocks.append({"type": "paragraph", "text": paragraph.layout.text_anchor.content if paragraph.layout.text_anchor else ""})
        for table in page.tables:
            blocks.append({"type": "table", "rows": len(table.body_rows), "columns": len(table.header_rows[0].cells) if table.header_rows else 0})
    return LayoutResponse(blocks=normalize_blocks(blocks), raw={"provider": "google_document_ai", "document": document.to_json()})
