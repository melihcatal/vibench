import boto3
import json
from storage_client import get_s3_client
from typing import List


def asset_metadata_embedding(bucket: str, key: str) -> List[float]:
    s3_client = get_s3_client()
    head_response = s3_client.head_object(Bucket=bucket, Key=key)
    metadata_text = " ".join(
        [f"{k}={v}" for k, v in head_response.get("Metadata", {}).items()]
    )
    obj_response = s3_client.get_object(Bucket=bucket, Key=key)
    text_content = obj_response["Body"].read().decode("utf-8")
    input_text = f"{metadata_text} {text_content}".strip()
    bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
    body = json.dumps({"inputText": input_text})
    model_id = "amazon.titan-embed-text-v1"
    response = bedrock_client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )
    result = json.loads(response["body"].read())
    return result["embedding"]
