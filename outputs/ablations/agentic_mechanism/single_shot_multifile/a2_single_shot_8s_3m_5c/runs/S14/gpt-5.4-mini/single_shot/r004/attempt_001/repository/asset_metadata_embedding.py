from typing import List

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from storage_models import AssetMetadataEmbeddingResult

BEDROCK_EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v2:0"


def embed_asset_metadata_and_text(bucket: str, key: str, metadata_text: str) -> AssetMetadataEmbeddingResult:
    client = boto3.client("bedrock-runtime")
    try:
        response = client.invoke_model(modelId=BEDROCK_EMBEDDING_MODEL_ID, body=__import__("json").dumps({"inputText": metadata_text}))
        payload = __import__("json").loads(response["body"].read())
        embedding = payload.get("embedding", [])
        return AssetMetadataEmbeddingResult(bucket=bucket, key=key, embedding=[float(x) for x in embedding], dimensions=len(embedding))
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(f"embedding failed with {BEDROCK_EMBEDDING_MODEL_ID}: {exc}") from exc


__all__ = ["embed_asset_metadata_and_text"]
