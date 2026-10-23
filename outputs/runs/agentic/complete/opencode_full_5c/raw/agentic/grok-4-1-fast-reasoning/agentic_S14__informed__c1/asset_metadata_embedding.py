from storage_client import s3_config
import boto3
import json
from typing import List


def generate_embedding_for_asset(bucket: str, key: str) -> List[float]:
    s3_client = boto3.client("s3", **s3_config)
    head_resp = s3_client.head_object(Bucket=bucket, Key=key)
    metadata_str = json.dumps(head_resp.get("Metadata", {}))
    get_resp = s3_client.get_object(Bucket=bucket, Key=key)
    text_content = get_resp["Body"].read().decode("utf-8", errors="ignore")[:6000]
    input_text = f"Metadata: {metadata_str}\\n\\nContent: {text_content}"
    bedrock_client = boto3.client("bedrock-runtime", **s3_config)
    body = json.dumps({"inputText": input_text})
    model_id = "amazon.titan-embed-text-v2:0"
    resp = bedrock_client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )
    resp_body = json.loads(resp["body"].read())
    return resp_body["embedding"]
