import os
from typing import Dict

import boto3


def summarize_asset_content(text: str, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0") -> Dict:
    """
    Summarize content extracted from a stored asset using Amazon Bedrock.
    """
    bedrock = boto3.client(
        "bedrock-runtime",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    prompt = f"Summarize the following text:\n\n{text}\n\nSummary:"

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}],
    }

    response = bedrock.invoke_model(
        modelId=model_id,
        body=bytes(str(body).replace("'", '"'), "utf-8"),
    )

    response_body = eval(response["body"].read().decode())
    return {"summary": response_body["content"][0]["text"]}