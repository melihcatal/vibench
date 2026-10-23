import boto3
import json
from storage_client import get_s3_client


def stored_asset_summary(bucket: str, key: str, max_tokens: int = 150) -> str:
    s3_client = get_s3_client()
    response = s3_client.get_object(Bucket=bucket, Key=key)
    content = response["Body"].read().decode("utf-8")
    prompt = f"Summarize this content:\n\n{content}"
    bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ],
        }
    )
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    invoke_response = bedrock_client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )
    result = json.loads(invoke_response["body"].read())
    return result["content"][0]["text"]
