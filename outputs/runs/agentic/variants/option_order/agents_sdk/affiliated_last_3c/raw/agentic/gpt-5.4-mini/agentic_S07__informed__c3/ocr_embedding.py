from __future__ import annotations

from typing import List, Optional

import boto3

from document_models import normalize_text


def embed_document_sections(sections: List[str], model_id: str = "amazon.titan-embed-text-v2:0", region_name: Optional[str] = None) -> List[List[float]]:
    client = boto3.client("bedrock-runtime", region_name=region_name)
    vectors: List[List[float]] = []
    for section in sections:
        payload = {"inputText": normalize_text(section)}
        response = client.invoke_model(body=str(payload).encode("utf-8"), modelId=model_id, accept="application/json", contentType="application/json")
        body = response["body"].read().decode("utf-8")
        vectors.append([float(x) for x in __import__("json").loads(body).get("embedding", [])])
    return vectors
