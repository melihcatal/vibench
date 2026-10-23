import json
from typing import Any, Dict

import boto3


def extract_document_fields(payload: Dict[str, Any]) -> Dict[str, Any]:
    client = boto3.client("bedrock-runtime")
    model_id = payload.get("model_id", "anthropic.claude-3-haiku-20240307-v1:0")
    prompt = payload.get("text", "")
    response = client.converse(modelId=model_id, messages=[{"role": "user", "content": [{"text": f"Extract structured fields as JSON from this OCR text:\n{prompt}"}]}])
    content = response.get("output", {}).get("message", {}).get("content", [])
    return {"model_id": model_id, "content": content, "raw": response}


if __name__ == "__main__":
    import sys

    print(json.dumps(extract_document_fields(json.loads(sys.stdin.read())), ensure_ascii=False))
