import json
from typing import Any, Dict

import boto3


def embed_ocr_sections(payload: Dict[str, Any]) -> Dict[str, Any]:
    client = boto3.client("bedrock-runtime")
    model_id = payload.get("model_id", "amazon.titan-embed-text-v2:0")
    sections = payload.get("sections", [])
    embeddings = []
    for section in sections:
        response = client.invoke_model(modelId=model_id, body=json.dumps({"inputText": section}).encode("utf-8"))
        embeddings.append({"section": section, "raw": response.read().decode("utf-8") if hasattr(response, "read") else response})
    return {"model_id": model_id, "embeddings": embeddings}


if __name__ == "__main__":
    import sys

    print(json.dumps(embed_ocr_sections(json.loads(sys.stdin.read())), ensure_ascii=False))
