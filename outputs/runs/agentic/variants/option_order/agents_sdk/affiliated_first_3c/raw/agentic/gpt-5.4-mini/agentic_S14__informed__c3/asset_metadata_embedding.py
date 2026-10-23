from __future__ import annotations

import json
from typing import Any

import boto3

from storage_models import EmbeddingRequest


AWS_BEDROCK_RUNTIME = boto3.client("bedrock-runtime")
EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v2:0"


def embed_asset_metadata(bucket: str, key: str, extracted_text: str = "", extra_metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    request = EmbeddingRequest(bucket=bucket, key=key, extracted_text=extracted_text, extra_metadata=extra_metadata or {})
    payload = {
        "bucket": request.bucket,
        "key": request.key,
        "text": request.extracted_text,
        "metadata": request.extra_metadata,
    }
    response = AWS_BEDROCK_RUNTIME.invoke_model(
        modelId=EMBEDDING_MODEL_ID,
        body=json.dumps({"inputText": json.dumps(payload)}),
        accept="application/json",
        contentType="application/json",
    )
    body = json.loads(response["body"].read())
    return {"bucket": request.bucket, "key": request.key, "embedding": body.get("embedding", []), "text": request.extracted_text, "metadata": request.extra_metadata}
