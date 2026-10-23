from google.cloud import documentai

from document_client import build_processor_name, get_config, get_document_ai_client
from document_models import normalize_blocks


def extract_layout(image_bytes: bytes, mime_type: str = "image/png"):
    cfg = get_config()
    client = get_document_ai_client()
    name = build_processor_name(cfg["project_id"], cfg["location"], cfg["processor_id"])
    raw_document = documentai.RawDocument(content=image_bytes, mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    response = client.process_document(request=request)
    pages = response.document.pages
    blocks = []
    for page in pages:
        for block in page.blocks:
            blocks.append({"type": "block", "text": response.document.text[block.layout.text_anchor.text_segments[0].start_index:block.layout.text_anchor.text_segments[0].end_index]})
    return normalize_blocks(blocks)
