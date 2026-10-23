from typing import Any, Dict, Union

from document_client import textract_client
from document_models import collect_key_values, normalize_blocks


def extract_key_values(document: Union[str, bytes, Dict[str, Any]]) -> Dict[str, Any]:
    client = textract_client()
    if isinstance(document, bytes):
        response = client.analyze_document(Document={"Bytes": document}, FeatureTypes=["FORMS"])
    else:
        response = client.analyze_document(Document=document, FeatureTypes=["FORMS"])
    blocks = normalize_blocks(response.get("Blocks", []))
    return {"key_values": collect_key_values(blocks), "blocks": blocks, "raw": response}
