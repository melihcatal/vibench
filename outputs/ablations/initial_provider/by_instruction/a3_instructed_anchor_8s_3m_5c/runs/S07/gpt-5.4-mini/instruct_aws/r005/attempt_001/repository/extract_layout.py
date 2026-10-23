import json
from typing import Any, Dict

from document_client import load_document_request, make_textract_client, s3_document_reference
from document_models import normalize_text


def extract_layout(payload: Dict[str, Any]) -> Dict[str, Any]:
    request = load_document_request(payload)
    client = make_textract_client(request.aws_region)
    response = client.analyze_document(Document=s3_document_reference(request), FeatureTypes=["LAYOUT"])
    blocks = []
    for block in response.get("Blocks", []):
        if block.get("BlockType") in {"LAYOUT_TEXT", "LAYOUT_TITLE", "LAYOUT_SECTION_HEADER", "LAYOUT_LIST", "LAYOUT_FIGURE", "LAYOUT_TABLE", "LAYOUT_KEY_VALUE"}:
            blocks.append({"type": block.get("BlockType"), "text": normalize_text(block.get("Text")), "page": int(block.get("Page", 1)), "confidence": float(block.get("Confidence", 0.0))})
    return {"layout": blocks, "raw": response}


if __name__ == "__main__":
    import sys

    print(json.dumps(extract_layout(json.loads(sys.stdin.read())), ensure_ascii=False))
