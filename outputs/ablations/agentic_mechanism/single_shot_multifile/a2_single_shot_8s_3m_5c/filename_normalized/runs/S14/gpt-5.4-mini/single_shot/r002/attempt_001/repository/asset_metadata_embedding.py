import json
import os
from typing import List

import boto3
from storage_client import get_s3_client, resolve_bucket_name, resolve_object_key
from storage_models import AssetMetadataEmbeddingRequest, AssetMetadataEmbeddingResponse

AWS_BEDROCK_EMBED_MODEL_ID = os.getenv("AWS_BEDROCK_EMBED_MODEL_ID", "amazon.titan-embed-text-v2:0")


def embed_asset_metadata(request: AssetMetadataEmbeddingRequest) -> AssetMetadataEmbeddingResponse:
    bucket = resolve_bucket_name(request.bucket)
    key = resolve_object_key(request.key)
    client = boto3.client("bedrock-runtime")
    payload = json.dumps({"inputText": f"{json.dumps(request.metadata, sort_keys=True)}\n{request.extracted_text}"})
    resp = client.invoke_model(modelId=AWS_BEDROCK_EMBED_MODEL_ID, body=payload.encode("utf-8"))
    data = json.loads(resp["body"].read())
    vector = data.get("embedding", data.get("vector", []))
    return AssetMetadataEmbeddingResponse(bucket=bucket, key=key, vector=vector, dimensions=len(vector), provider="aws-bedrock")
