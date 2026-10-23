import json
from typing import Any, Dict

from document_client import load_document_request, make_textract_client, s3_document_reference
from document_models import normalize_text


def extract_key_values(payload: Dict[str, Any]) -> Dict[str, Any]:
    request = load_document_request(payload)
    client = make_textract_client(request.aws_region)
    response = client.analyze_document(Document=s3_document_reference(request), FeatureTypes=["FORMS"])
    pairs = []
    for block in response.get("Blocks", []):
        if block.get("BlockType") == "KEY_VALUE_SET":
            entity_types = set(block.get("EntityTypes", []))
            if "KEY" in entity_types:
                pairs.append({"key": normalize_text(block.get("Text")), "value": "", "confidence": float(block.get("Confidence", 0.0))})
    return {"key_values": pairs, "raw": response}


if __name__ == "__main__":
    import sys

    print(json.dumps(extract_key_values(json.loads(sys.stdin.read())), ensure_ascii=False))
