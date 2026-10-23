from typing import List

import boto3

from document_models import OcrResult


def embed_document_sections(result: OcrResult) -> List[List[float]]:
    bedrock = boto3.client("bedrock-runtime")
    embeddings: List[List[float]] = []
    for line in result.lines[:50]:
        response = bedrock.invoke_model(modelId="amazon.titan-embed-text-v1", body=("{\"inputText\": \"" + line.text.replace('"', '\\"') + "\"}").encode("utf-8"))
        body = response.get("body")
        if body is not None:
            payload = body.read().decode("utf-8")
            import json
            data = json.loads(payload)
            embeddings.append(data.get("embedding", []))
    return embeddings
