import base64
from typing import Any, Dict, List

from document_client import get_textract_client
from document_models import OCRRequest, OCRResponse, collect_block_text


def _ensure_bytes(document: Any) -> bytes:
    if isinstance(document, bytes):
        return document
    if isinstance(document, str):
        try:
            return base64.b64decode(document)
        except Exception:
            with open(document, "rb") as f:
                return f.read()
    raise TypeError("document must be bytes or a base64 string or file path")


def extract_text(document: Any) -> OCRResponse:
    document_bytes = _ensure_bytes(document)
    client = get_textract_client()
    response = client.detect_document_text(Document={"Bytes": document_bytes})
    blocks: List[Dict[str, Any]] = response.get("Blocks", [])
    return OCRResponse(text=collect_block_text(blocks, "LINE"), blocks=blocks)


def handle(document: Any) -> Dict[str, Any]:
    result = extract_text(document)
    return {"text": result.text, "blocks": result.blocks}
