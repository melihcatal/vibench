import json
from typing import Any, Dict

from document_client import load_document_request, make_textract_client, s3_document_reference
from document_models import normalize_text


def extract_text(payload: Dict[str, Any]) -> Dict[str, Any]:
    request = load_document_request(payload)
    client = make_textract_client(request.aws_region)
    response = client.detect_document_text(Document=s3_document_reference(request))
    lines = []
    full_text = []
    for block in response.get("Blocks", []):
        if block.get("BlockType") == "LINE":
            text = normalize_text(block.get("Text"))
            if text:
                lines.append({"text": text, "confidence": float(block.get("Confidence", 0.0)), "page": int(block.get("Page", 1))})
                full_text.append(text)
    return {"text": "\n".join(full_text), "lines": lines, "raw": response}


if __name__ == "__main__":
    import sys

    print(json.dumps(extract_text(json.loads(sys.stdin.read())), ensure_ascii=False))
