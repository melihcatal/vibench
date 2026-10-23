import boto3
import json
from typing import List
from storage_client import get_aws_client_kwargs


def asset_metadata_embedding(bucket: str, object_key: str) -> List[float]:
    kwargs = get_aws_client_kwargs()
    s3_client = boto3.client("s3", **kwargs)
    head_response = s3_client.head_object(Bucket=bucket, Key=object_key)
    metadata = dict(head_response.get("Metadata", {}))
    content_type = head_response.get("ContentType", "")
    size = head_response["ContentLength"]
    get_response = s3_client.get_object(Bucket=bucket, Key=object_key)
    text = get_response["Body"].read().decode("utf-8", errors="ignore")[:8192]
    combined_text = (
        f"Object key: {object_key}\\n"
        f"Size: {size}\\n"
        f"Content-Type: {content_type}\\n"
        f"Metadata: {json.dumps(metadata)}\\n"
        f"Content preview: {text}"
    )
    bedrock_client = boto3.client("bedrock-runtime", **kwargs)
    body = json.dumps({"inputText": combined_text})
    model_id = "amazon.titan-embed-text-v2:0"
    invoke_response = bedrock_client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )
    result = json.loads(invoke_response["body"].read())
    return result["embedding"]
