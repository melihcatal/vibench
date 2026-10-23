import json
from typing import Any, Dict

from document_client import load_document_request, make_textract_client, s3_document_reference
from document_models import normalize_text


def extract_tables(payload: Dict[str, Any]) -> Dict[str, Any]:
    request = load_document_request(payload)
    client = make_textract_client(request.aws_region)
    response = client.analyze_document(Document=s3_document_reference(request), FeatureTypes=["TABLES"])
    tables = []
    for block in response.get("Blocks", []):
        if block.get("BlockType") == "TABLE":
            tables.append({"text": normalize_text(block.get("Text")), "page": int(block.get("Page", 1)), "confidence": float(block.get("Confidence", 0.0)), "relationships": block.get("Relationships", [])})
    return {"tables": tables, "raw": response}


if __name__ == "__main__":
    import sys

    print(json.dumps(extract_tables(json.loads(sys.stdin.read())), ensure_ascii=False))
