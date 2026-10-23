"""
Summarize content extracted from a stored asset using AWS Bedrock (Anthropic Claude).

Provider: AWS Bedrock via boto3
- Uses boto3.client('bedrock-runtime') for AWS Bedrock model inference
- Uses model id: anthropic.claude-3-sonnet-20240229-v1:0 (Anthropic Claude 3 Sonnet)
- AWS Bedrock managed inference endpoint with Converse API
"""

import json
import logging
from typing import Any, Dict, Optional

from storage_client import get_bedrock_runtime_client

logger = logging.getLogger(__name__)

BEDROCK_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"
BEDROCK_SUMMARY_MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"


def summarize_extracted_content(
    extracted_text: str,
    max_tokens: int = 1024,
    temperature: float = 0.3,
    model_id: str = BEDROCK_SUMMARY_MODEL_ID,
    system_prompt: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate a summary of extracted document text using AWS Bedrock.

    Uses the Anthropic Claude model family via AWS Bedrock Converse API
    to produce concise summaries of document content.

    Provider signals:
    - boto3 bedrock-runtime client (AWS Bedrock managed inference)
    - Model ID: anthropic.claude-3-haiku-20240307-v1:0 or anthropic.claude-3-sonnet-20240229-v1:0
    - AWS Bedrock Converse API for model inference
    - Anthropic Claude model family on AWS Bedrock
    """
    bedrock_client = get_bedrock_runtime_client()

    default_system = (
        "You are a document analysis assistant. Provide a concise, "
        "accurate summary of the provided text. Focus on key facts, "
        "entities, dates, and main conclusions."
    )

    conversation = [
        {
            "role": "user",
            "content": [
                {
                    "text": f"Please summarize the following document content:\n\n{extracted_text}"
                }
            ],
        }
    ]

    inference_config = {
        "maxTokens": max_tokens,
        "temperature": temperature,
    }

    logger.info(
        "Summarizing %d chars via AWS Bedrock model %s",
        len(extracted_text), model_id,
    )

    converse_kwargs = {
        "modelId": model_id,
        "messages": conversation,
        "inferenceConfig": inference_config,
    }

    if system_prompt:
        converse_kwargs["system"] = [{"text": system_prompt}]
    else:
        converse_kwargs["system"] = [{"text": default_system}]

    response = bedrock_client.converse(**converse_kwargs)

    output_content = response.get("output", {}).get("message", {}).get("content", [])
    summary_text = ""
    for content_block in output_content:
        if "text" in content_block:
            summary_text += content_block["text"]

    stop_reason = response.get("stopReason", "")
    usage = response.get("usage", {})

    return {
        "summary": summary_text,
        "stop_reason": stop_reason,
        "input_tokens": usage.get("inputTokens", 0),
        "output_tokens": usage.get("outputTokens", 0),
        "model_id": model_id,
    }


def summarize_asset_with_metadata(
    asset_text: str,
    asset_metadata: Optional[Dict[str, str]] = None,
    model_id: str = BEDROCK_SUMMARY_MODEL_ID,
) -> Dict[str, Any]:
    """
    Summarize an asset using both its extracted text and metadata.

    Provides context about the asset's storage metadata to enrich
    the summary with file-specific information.

    Provider signals:
    - AWS Bedrock bedrock-runtime client
    - Anthropic Claude 3 Haiku model: anthropic.claude-3-haiku-20240307-v1:0
    - AWS Bedrock Converse API
    """
    bedrock_client = get_bedrock_runtime_client()

    metadata_context = ""
    if asset_metadata:
        metadata_pairs = ", ".join(f"{k}: {v}" for k, v in asset_metadata.items())
        metadata_context = f"\nAsset metadata: {metadata_pairs}"

    prompt = (
        f"Summarize the following asset content and its associated metadata.{metadata_context}\n\n"
        f"Document content:\n{asset_text}"
    )

    conversation = [
        {
            "role": "user",
            "content": [{"text": prompt}],
        }
    ]

    system_text = (
        "You are a digital asset management assistant. Summarize the "
        "asset content concisely, noting key themes, entities, and "
        "any notable metadata context."
    )

    logger.info(
        "Summarizing asset with metadata via AWS Bedrock model %s", model_id,
    )

    response = bedrock_client.converse(
        modelId=model_id,
        messages=conversation,
        inferenceConfig={
            "maxTokens": 1024,
            "temperature": 0.3,
        },
        system=[{"text": system_text}],
    )

    output_content = response.get("output", {}).get("message", {}).get("content", [])
    summary_text = ""
    for content_block in output_content:
        if "text" in content_block:
            summary_text += content_block["text"]

    usage = response.get("usage", {})

    return {
        "summary": summary_text,
        "input_tokens": usage.get("inputTokens", 0),
        "output_tokens": usage.get("outputTokens", 0),
        "model_id": model_id,
    }
