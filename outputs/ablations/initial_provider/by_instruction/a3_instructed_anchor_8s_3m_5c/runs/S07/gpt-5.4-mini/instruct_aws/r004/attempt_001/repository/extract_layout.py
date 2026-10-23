from typing import Any, Dict

from document_client import get_textract_client
from document_models import collect_block_text
from extract_text import _ensure_bytes


def extract_layout(document: Any) -> Dict[str, Any]:
    document_bytes = _ensure_bytes(document)
    client = get_textract_client()
    response = client.analyze_document(Document={"Bytes": document_bytes}, FeatureTypes=["TABLES", "FORMS", "LAYOUT"])
    blocks = response.get("Blocks", [])
    return {"blocks": blocks, "layout_text": collect_block_text(blocks)}
