from __future__ import annotations

import boto3


def crypto_audit_embedding(note: str, region_name: str | None = None) -> dict:
    client = boto3.client("bedrock-runtime", region_name=region_name)
    body = {"inputText": note}
    response = client.invoke_model(modelId="amazon.titan-embed-text-v2:0", body=str(body).encode("utf-8"), contentType="application/json", accept="application/json")
    return {"provider": "Amazon Bedrock Runtime", "model_id": "amazon.titan-embed-text-v2:0", "response_metadata": response.get("ResponseMetadata", {})}
