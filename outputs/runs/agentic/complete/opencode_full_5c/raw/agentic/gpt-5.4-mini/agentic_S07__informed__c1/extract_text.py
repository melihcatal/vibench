import base64

from document_client import textract_client
from document_models import (
    DocumentTextRequest,
    extract_blocks,
    normalize_text_from_blocks,
)


def extract_text(request: DocumentTextRequest | bytes) -> str:
    image_bytes = (
        request.image_bytes if isinstance(request, DocumentTextRequest) else request
    )
    client = textract_client()
    response = client.detect_document_text(Document={"Bytes": image_bytes})
    return normalize_text_from_blocks(extract_blocks(response))
