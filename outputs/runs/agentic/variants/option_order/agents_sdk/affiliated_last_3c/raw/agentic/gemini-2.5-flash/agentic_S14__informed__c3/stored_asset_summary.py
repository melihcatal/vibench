import os
import boto3
import json

def summarize_content_with_bedrock(text_content: str, max_tokens: int = 500) -> str:
    """
    Summarizes content extracted from a stored asset using an LLM on Amazon Bedrock (Anthropic Claude).

    Args:
        text_content (str): The text content to summarize.
        max_tokens (int): The maximum number of tokens for the summary.

    Returns:
        str: The summarized text.
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set in environment variables.")

    bedrock_runtime_client = boto3.client(
        "bedrock-runtime",
        region_name=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    # Using Anthropic Claude on Bedrock
    model_id = "anthropic.claude-v2"
    prompt = f"Human: Summarize the following document concisely:

{text_content}

Assistant:"

    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": max_tokens,
        "temperature": 0.5,
        "top_p": 0.9
    })

    response = bedrock_runtime_client.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=body
    )

    response_body = json.loads(response['body'].read())
    return response_body['completion'].strip()
