"""Summarize content extracted from a stored asset using AWS Bedrock.

Uses boto3 to call the AWS Bedrock service (model: anthropic.claude-3-haiku-20240307-v1:0)
to generate summaries of document text extracted from S3-stored assets.
Requires AWS credentials in environment variables:
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
"""

import json
from storage_client import get_s3_client
from storage_models import AssetSummary

BEDROCK_MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"


def _build_bedrock_prompt(text, summary_length="medium"):
    """Build a prompt for Claude to summarize the given text."""
    length_map = {
        "short": "one or two sentences",
        "medium": "a concise paragraph",
        "long": "two or three detailed paragraphs",
    }
    length_instruction = length_map.get(summary_length, length_map["medium"])

    prompt = f"""You are an expert document analyst. Summarize the following document content in {length_instruction}. Also extract key phrases and named entities.

Document content:
---
{text}
---

Provide your response as a JSON object with the following structure:
{{
  "summary": "...",
  "key_phrases": ["phrase1", "phrase2", ...],
  "entities": ["entity1", "entity2", ...]
}}"""

    return prompt


def stored_asset_summary(bucket, key, summary_length="medium", region=None,
                         endpoint_url=None):
    """Summarize content of a stored S3 asset using AWS Bedrock (Claude 3 Haiku).

    Downloads the text content of the object and sends it to the
    anthropic.claude-3-haiku-20240307-v1:0 model via AWS Bedrock for summarization.

    Args:
        bucket: S3 bucket name.
        key: S3 object key of the asset.
        summary_length: Desired summary length ("short", "medium", "long").
        region: Optional AWS region override.
        endpoint_url: Optional custom S3 endpoint.

    Returns:
        AssetSummary containing the generated summary, key phrases, and entities.

    Raises:
        botocore.exceptions.ClientError: If Bedrock invocation fails.
    """
    s3_client = get_s3_client(region=region, endpoint_url=endpoint_url)

    # Retrieve object content from S3
    response = s3_client.get_object(Bucket=bucket, Key=key)
    raw_text = response["Body"].read().decode("utf-8", errors="replace")

    return _summarize_text(raw_text, bucket, key, summary_length, region=region)


def _summarize_text(text, bucket="", key="", summary_length="medium", region=None):
    """Send text to AWS Bedrock Claude model for summarization."""
    import boto3

    bedrock_region = region or "us-east-1"

    session = boto3.Session(
        aws_access_key_id=__import__("os").environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=__import__("os").environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=bedrock_region,
    )
    bedrock_client = session.client("bedrock-runtime", region_name=bedrock_region)

    prompt = _build_bedrock_prompt(text, summary_length)

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    })

    response = bedrock_client.invoke_model(
        modelId=BEDROCK_MODEL_ID,
        body=body,
    )

    result_body = json.loads(response["body"].read())
    assistant_text = result_body["content"][0]["text"]

    # Parse JSON from the assistant response
    try:
        summary_data = json.loads(assistant_text)
    except json.JSONDecodeError:
        # Fallback: use raw text as summary
        summary_data = {
            "summary": assistant_text.strip(),
            "key_phrases": [],
            "entities": [],
        }

    word_count = len(text.split())

    return AssetSummary(
        object_uri=f"s3://{bucket}/{key}" if bucket and key else "unknown",
        summary=summary_data.get("summary", ""),
        key_phrases=summary_data.get("key_phrases", []),
        entities=summary_data.get("entities", []),
        model_id=BEDROCK_MODEL_ID,
        word_count=word_count,
    )
