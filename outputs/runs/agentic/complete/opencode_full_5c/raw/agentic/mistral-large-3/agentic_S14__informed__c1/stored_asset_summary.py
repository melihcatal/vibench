import os
from typing import Optional

import boto3
from botocore.exceptions import ClientError


def summarize_stored_asset_content(
    text: str,
    model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0",
    max_tokens: int = 1000,
) -> dict:
    """
    Summarizes content extracted from a stored asset using Amazon Bedrock.

    Args:
        text: Text content to summarize.
        model_id: Bedrock model ID for summarization.
        max_tokens: Maximum number of tokens in the summary.

    Returns:
        Dictionary containing the summary and metadata.
    """
    bedrock_client = boto3.client("bedrock-runtime")

    try:
        prompt = f"Please summarize the following text:\n\n{text}\n\nSummary:"

        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=bytes(
                f'{{"prompt": "{prompt}", "max_tokens_to_sample": {max_tokens}}}',
                encoding="utf-8",
            ),
            contentType="application/json",
            accept="application/json",
        )

        result = response["body"].read().decode("utf-8")
        summary = eval(result).get("completion", "")

        return {
            "summary": summary,
            "model_id": model_id,
            "provider": "aws_bedrock",
        }
    except ClientError as e:
        raise Exception(f"Failed to summarize content: {e}")
