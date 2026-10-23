import boto3
import os
import json
from botocore.exceptions import ClientError


def summarize_asset_content(text, model_id="anthropic.claude-3-sonnet-20240229-v1:0"):
    """
    Summarize content extracted from a stored asset using Amazon Bedrock.

    Args:
        text: Text content to summarize
        model_id: Bedrock model ID (default: Claude 3 Sonnet)

    Returns:
        dict: Summary results including summary text and model information
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise EnvironmentError(
            "AWS credentials not found. Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
        )

    bedrock_runtime = boto3.client(
        "bedrock-runtime",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )

    prompt = f"""Please provide a concise summary of the following text:

{text}

Summary:"""

    try:
        if model_id.startswith("anthropic."):
            body = json.dumps(
                {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 500,
                    "messages": [{"role": "user", "content": prompt}],
                }
            )
        else:
            body = json.dumps({"prompt": prompt, "max_tokens": 500})

        response = bedrock_runtime.invoke_model(modelId=model_id, body=body)

        response_body = json.loads(response["body"].read())

        if model_id.startswith("anthropic."):
            summary_text = response_body["content"][0]["text"]
        else:
            summary_text = response_body["completion"]

        return {
            "original_length": len(text),
            "summary": summary_text.strip(),
            "summary_length": len(summary_text.strip()),
            "model_id": model_id,
            "provider": "Amazon Bedrock",
        }
    except ClientError as e:
        raise Exception(f"Failed to summarize content using Amazon Bedrock: {e}")
