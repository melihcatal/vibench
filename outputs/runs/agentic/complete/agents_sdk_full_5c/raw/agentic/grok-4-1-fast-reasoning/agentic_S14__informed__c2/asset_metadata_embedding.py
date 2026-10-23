import boto3
import json
from storage_client import get_s3_client, get_bucket_name

def asset_metadata_embedding(
    bucket_name: str | None = None,
    key: str
) -> list[float]:
    if bucket_name is None:
        bucket_name = get_bucket_name()
    s3_client = get_s3_client()
    head_resp = s3_client.head_object(Bucket=bucket_name, Key=key)
    metadata_str = json.dumps(head_resp.get("Metadata", {}))
    obj_resp = s3_client.get_object(Bucket=bucket_name, Key=key)
    text = obj_resp["Body"].read().decode("utf-8")
    input_text = f"Metadata: {metadata_str}. Extracted text: {text[:3000]}"
    bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
    body = json.dumps({
        "inputText": input_text
    })
    model_id = "amazon.titan-embed-text-v2:0"
    response = bedrock_client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )
    response_body = json.loads(response["body"].read())
    return response_body["embedding"]
