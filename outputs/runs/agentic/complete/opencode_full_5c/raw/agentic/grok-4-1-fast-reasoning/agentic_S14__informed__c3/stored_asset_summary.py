import boto3
import json
import os
from storage_client import download_text


def summarize_asset(key: str) -> str:
    text = download_text(key)
    region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    bedrock = boto3.client("bedrock-runtime", region_name=region)
    prompt = f"Summarize the following content concisely:\n\n{text}"
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 512,
            "messages": [{"role": "user", "content": prompt}],
        }
    )
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    response = bedrock.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )
    response_body = json.loads(response["body"].read())
    return response_body["content"][0]["text"]
