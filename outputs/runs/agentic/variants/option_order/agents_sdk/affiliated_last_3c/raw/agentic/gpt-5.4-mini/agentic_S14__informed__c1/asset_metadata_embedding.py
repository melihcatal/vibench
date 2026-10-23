from __future__ import annotations

import boto3

from storage_models import EmbeddingResult


_EMBED_MODEL_ID = "amazon.titan-embed-text-v2:0"


def embed_asset_metadata_and_text(metadata_text: str) -> EmbeddingResult:
    client = boto3.client("bedrock-runtime")
    response = client.invoke_model(
        modelId=_EMBED_MODEL_ID,
        body=f'{{"inputText": {metadata_text!r}}}',
        contentType="application/json",
        accept="application/json",
    )
    body = response["body"].read().decode("utf-8")
    raw = {"body": body}
    return EmbeddingResult(text=metadata_text, vector=[], raw=raw)
