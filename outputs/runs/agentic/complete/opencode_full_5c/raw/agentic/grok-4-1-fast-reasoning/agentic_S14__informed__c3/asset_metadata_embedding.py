import boto3
import json
import os
from storage_client import download_text, get_s3_client, get_bucket
from object_metadata import get_object_metadata
from storage_models import ObjectMetadata
from botocore.exceptions import ClientError


def embed_asset_metadata(key: str) -> list[float]:
    metadata: ObjectMetadata = get_object_metadata(key)
    text = download_text(key)
    combined_text = f"Metadata: size={metadata.size}, etag={metadata.etag}, last_modified={metadata.last_modified}, content_type={metadata.content_type}. Text: {text}"
    region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    bedrock = boto3.client("bedrock-runtime", region_name=region)
    body = json.dumps({"inputText": combined_text})
    model_id = "amazon.titan-embed-text-v2:0"
    response = bedrock.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )
    response_body = json.loads(response["body"].read())
    return response_body["embedding"]
