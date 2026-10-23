from document_client import create_client, load_config, process_bytes
from document_models import (
    LayoutExtractionRequest,
    blocks_from_document,
    lines_from_document,
)


def extract_layout(request: LayoutExtractionRequest):
    config = load_config()
    client = create_client()
    content = open(request.image_path, "rb").read()
    document = process_bytes(client, config, content, request.mime_type)
    return {
        "blocks": blocks_from_document(document),
        "lines": lines_from_document(document),
    }
