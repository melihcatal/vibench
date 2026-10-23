import os
from typing import Optional

import boto3
from botocore.exceptions import ClientError


def stored_asset_summary(
    text: str, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"
) -> str:
    """
    Summarizes content extracted from a stored asset using Amazon Bedrock.

    Args:
        text: Text content to summarize.
        model_id: Bedrock model ID (default: anthropic.claude-3-sonnet-20240229-v1:0).

    Returns:
        str: Generated summary of the text.
    """
    bedrock = boto3.client(
        "bedrock-runtime",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    prompt = f"Please summarize the following text:\n\n{text}\n\nSummary:"

    try:
        response = bedrock.invoke_model(
            modelId=model_id,
            body=bytes(f'{{"prompt":"{prompt}","max_tokens_to_sample":500}}', "utf-8"),
            contentType="application/json",
            accept="application/json",
        )
        result = response["body"].read().decode("utf-8")
        return eval(result).get("completion", "")
    except ClientError as e:
        raise Exception(f"Failed to generate summary using Amazon Bedrock: {e}")
