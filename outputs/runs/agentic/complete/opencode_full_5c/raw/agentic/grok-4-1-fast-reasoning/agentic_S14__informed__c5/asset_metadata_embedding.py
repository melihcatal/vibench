import boto3
import json
from storage_client import get_s3_client
from typing import List


def asset_metadata_embedding(bucket_name: str, object_name: str) -> List[float]:
    s3_client = get_s3_client(region="us-east-1")
    head_response = s3_client.head_object(Bucket=bucket_name, Key=object_name)
    metadata_str = json.dumps(dict(head_response.get("Metadata", {})))
    obj_response = s3_client.get_object(Bucket=bucket_name, Key=object_name)
    text_excerpt = obj_response["Body"].read().decode("utf-8")[:1000]
    input_text = f"{metadata_str} ||| {text_excerpt}"
    bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
    body = json.dumps({"inputText": input_text})
    model_id = "amazon.titan-embed-text-v2:0"
    response = bedrock_client.invoke_model(
        modelId=model_id,
        body=body,
        contentType="application/json",
        accept="application/json",
    )
    result = json.loads(response["body"].read())
    return result["embedding"]
