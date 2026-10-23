"""
stored_asset_summary.py - Summarize content extracted from a stored asset
using Amazon Bedrock with Anthropic Claude model.

Uses the boto3 SDK (Amazon Bedrock Runtime) with model
anthropic.claude-3-sonnet-20240229-v1:0.
Auth env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""
from __future__ import annotations

import json
import os
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from storage_models import SummaryRequest, SummaryResponse


def stored_asset_summary(
    text: str,
    bucket: Optional[str] = None,
    key: Optional[str] = None,
    max_tokens: int = 512,
    model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0",
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region: Optional[str] = None,
) -> SummaryResponse:
    """
    Summarize extracted content from a stored asset using Amazon Bedrock
    with the Anthropic Claude model.

    Amazon Bedrock provides managed access to foundation models. This function
    uses the anthropic.claude-3-sonnet-20240229-v1:0 model via the
    Bedrock Runtime invoke_model API.

    Args:
        text: The extracted text content to summarize.
        bucket: Optional S3 bucket name of the source document.
        key: Optional S3 object key of the source document.
        max_tokens: Maximum tokens for the generated summary.
        model_id: Amazon Bedrock model ID (default: anthropic.claude-3-sonnet-20240229-v1:0).
        aws_access_key_id: Optional AWS access key ID override.
        aws_secret_access_key: Optional AWS secret access key override.
        region: Optional AWS region override.

    Returns:
        SummaryResponse with the generated summary and metadata.
    """
    request = SummaryRequest(
        text=text,
        bucket=bucket,
        key=key,
        max_tokens=max_tokens,
        model_id=model_id,
    )

    bedrock_region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    bedrock_runtime = boto3.client(
        "bedrock-runtime",
        region_name=bedrock_region,
        aws_access_key_id=aws_access_key_id or os.environ.get("AWS_ACCESS_KEY_ID", ""),
        aws_secret_access_key=aws_secret_access_key or os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
    )

    system_prompt = (
        "You are a professional document summarization assistant. "
        "Provide a concise, accurate summary of the following content. "
        "Focus on key findings, important data points, and actionable information. "
        "Use clear and structured language."
    )

    user_message = f"Please summarize the following document content:\n\n{request.text}"

    # Build the Anthropic Claude Messages API request body for Bedrock
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": request.max_tokens,
        "system": system_prompt,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_message,
                    }
                ],
            }
        ],
        "temperature": 0.3,
        "top_p": 0.9,
    }

    try:
        # Invoke the Anthropic Claude model via Amazon Bedrock Runtime
        response = bedrock_runtime.invoke_model(
            modelId=request.model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(request_body),
        )

        response_body = json.loads(response["body"].read())

        # Extract summary from Anthropic Claude response format
        content_blocks = response_body.get("content", [])
        summary_text = ""
        tokens_used = 0

        for block in content_blocks:
            if block.get("type") == "text":
                summary_text += block.get("text", "")

        # Extract usage metadata from Anthropic response
        usage = response_body.get("usage", {})
        tokens_used = usage.get("output_tokens", 0) + usage.get("input_tokens", 0)

        return SummaryResponse(
            summary=summary_text.strip(),
            model_id=request.model_id,
            tokens_used=tokens_used,
            bucket=request.bucket,
            key=request.key,
        )

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        error_message = e.response.get("Error", {}).get("Message", str(e))
        raise RuntimeError(
            f"Amazon Bedrock (anthropic.claude-3-sonnet-20240229-v1:0) error [{error_code}]: {error_message}"
        )


def stored_asset_summary_with_fallback(
    text: str,
    bucket: Optional[str] = None,
    key: Optional[str] = None,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region: Optional[str] = None,
) -> SummaryResponse:
    """
    Summarize content using Amazon Bedrock Claude with automatic fallback
    from sonnet to haiku model if needed.

    Models tried in order:
    1. anthropic.claude-3-sonnet-20240229-v1:0
    2. anthropic.claude-3-haiku-20240307-v1:0
    """
    primary_model = "anthropic.claude-3-sonnet-20240229-v1:0"
    fallback_model = "anthropic.claude-3-haiku-20240307-v1:0"

    try:
        return stored_asset_summary(
            text=text,
            bucket=bucket,
            key=key,
            model_id=primary_model,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region=region,
        )
    except RuntimeError:
        return stored_asset_summary(
            text=text,
            bucket=bucket,
            key=key,
            model_id=fallback_model,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region=region,
        )
