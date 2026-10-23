from typing import Any, Dict, List

from document_client import get_textract_client
from extract_text import _ensure_bytes


def extract_key_values(document: Any) -> Dict[str, Any]:
    document_bytes = _ensure_bytes(document)
    client = get_textract_client()
    response = client.analyze_document(Document={"Bytes": document_bytes}, FeatureTypes=["FORMS"])
    blocks = response.get("Blocks", [])
    pairs: List[Dict[str, Any]] = [block for block in blocks if block.get("BlockType") in {"KEY_VALUE_SET", "WORD", "LINE"}]
    return {"key_values": pairs, "blocks": blocks}
