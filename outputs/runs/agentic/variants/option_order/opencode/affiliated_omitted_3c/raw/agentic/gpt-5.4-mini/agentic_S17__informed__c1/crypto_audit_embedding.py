import os
import json
from typing import Any, Dict, List

import boto3

from security_models import normalize_text


def embed_crypto_audit_notes(notes: List[str], model_id: str = "amazon.titan-embed-text-v2:0") -> Dict[str, Any]:
    client = boto3.client("bedrock-runtime")
    texts = [normalize_text(note) for note in notes]
    embeddings = []
    for text in texts:
        body = json.dumps({"inputText": text, "dimensions": 1024, "normalize": True})
        response = client.invoke_model(modelId=model_id, body=body, accept="application/json", contentType="application/json")
        payload = json.loads(response["body"].read())
        embeddings.append(payload.get("embedding", []))
    return {"provider": "aws-bedrock", "model_id": model_id, "notes": texts, "embeddings": embeddings}
