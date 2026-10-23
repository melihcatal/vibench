"""
Summarize content extracted from a stored asset.

Uses Amazon Bedrock with Anthropic Claude model as the concrete managed AI service.
Generates summaries of text content extracted from S3-stored documents.
"""

import json
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

from stored_document_ocr import TextractOCRResult, run_ocr_on_s3_object

# AWS Bedrock concrete model identifiers
BEDROCK_CLAUDE_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"
BEDROCK_CLAUDE_3_HAIKU_MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"
BEDROCK_CLAUDE_3_5_SONNET_MODEL_ID = "anthropic.claude-3-5-sonnet-20241022-v2:0"
BEDROCK_SERVICE_ENDPOINT = "bedrock-runtime"


DEFAULT_SUMMARY_SYSTEM_PROMPT = """You are a professional document summarization assistant.
Given the text content extracted from a document, provide a clear, concise summary.
Focus on key points, main arguments, conclusions, and important details.
Structure the summary with clear headings and bullet points where appropriate.
Keep the summary factual and do not add information not present in the source text."""


class AssetSummaryResult:
    """Result from asset content summarization via Amazon Bedrock."""

    def __init__(
        self,
        summary_text: str,
        model_id: str,
        input_tokens: int = 0,
        output_tokens: int = 0,
        raw_response: Optional[Dict[str, Any]] = None,
    ):
        self.summary_text = summary_text
        self.model_id = model_id
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.raw_response = raw_response or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary": self.summary_text,
            "model_id": self.model_id,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
        }


def _build_claude_converse_messages(
    text: str,
    system_prompt: str,
    max_summary_length: Optional[str] = None,
) -> tuple:
    """Build Claude Converse API messages from text and system prompt."""
    user_content = text

    if max_summary_length:
        user_content = (
            f"Please keep the summary to approximately {max_summary_length}. "
            f"\n\nDocument text:\n{text}"
        )
    else:
        user_content = f"Summarize the following document:\n\n{text}"

    messages = [{"role": "user", "content": [{"text": user_content}]}]
    system_content = [{"text": system_prompt}]

    return system_content, messages


def summarize_content(
    content: str,
    model_id: str = BEDROCK_CLAUDE_3_SONNET_MODEL_ID,
    system_prompt: Optional[str] = None,
    max_tokens: int = 2048,
    temperature: float = 0.3,
    max_summary_length: Optional[str] = None,
    client_config: Optional[Dict[str, Any]] = None,
) -> AssetSummaryResult:
    """
    Generate a summary of text content using Amazon Bedrock Claude model.

    Uses the Converse API (boto3 bedrock-runtime) for unified model invocation.

    Args:
        content: Text content to summarize.
        model_id: Bedrock model identifier (default: Claude 3 Sonnet).
        system_prompt: Optional custom system prompt.
        max_tokens: Maximum tokens for the summary.
        temperature: Generation temperature (0.0-1.0).
        max_summary_length: Optional target length description (e.g., "3 paragraphs").
        client_config: Optional boto3 client configuration overrides.

    Returns:
        AssetSummaryResult with the generated summary.

    Raises:
        ClientError: If Bedrock invocation fails.
        ValidationException: If input is invalid.
    """
    if not content or not content.strip():
        return AssetSummaryResult(
            summary_text="",
            model_id=model_id,
        )

    bedrock_runtime = boto3.client(
        "bedrock-runtime",
        region_name=client_config.get("region_name") if client_config else None,
    )

    system_prompt = system_prompt or DEFAULT_SUMMARY_SYSTEM_PROMPT
    system_content, messages = _build_claude_converse_messages(
        text=content,
        system_prompt=system_prompt,
        max_summary_length=max_summary_length,
    )

    inference_config = {
        "maxTokens": max_tokens,
        "temperature": temperature,
    }

    try:
        response = bedrock_runtime.converse(
            modelId=model_id,
            messages=messages,
            system=system_content,
            inferenceConfig=inference_config,
        )

        output_message = response.get("output", {}).get("message", {})
        summary_text = ""
        for content_block in output_message.get("content", []):
            if "text" in content_block:
                summary_text += content_block["text"]

        usage = response.get("usage", {})
        input_tokens = usage.get("inputTokens", 0)
        output_tokens = usage.get("outputTokens", 0)

        return AssetSummaryResult(
            summary_text=summary_text,
            model_id=model_id,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            raw_response=response,
        )

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "")
        raise ClientError(
            e.response,
            f"Bedrock summarization failed with model {model_id}: {e} (code: {error_code})",
        )


def summarize_stored_document(
    bucket: str,
    key: str,
    model_id: str = BEDROCK_CLAUDE_3_SONNET_MODEL_ID,
    system_prompt: Optional[str] = None,
    max_tokens: int = 2048,
    temperature: float = 0.3,
    ocr_feature_types: Optional[List[str]] = None,
    client_config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Full pipeline: OCR a stored document then summarize extracted content.

    Args:
        bucket: S3 bucket name.
        key: S3 object key.
        model_id: Bedrock model identifier.
        system_prompt: Optional custom system prompt.
        max_tokens: Maximum tokens for the summary.
        temperature: Generation temperature.
        ocr_feature_types: Textract features for OCR.
        client_config: Optional client configuration.

    Returns:
        Dictionary with OCR text, summary, and metadata.
    """
    ocr_result = run_ocr_on_s3_object(
        bucket=bucket,
        key=key,
        feature_types=ocr_feature_types,
        client_config=client_config,
    )

    summary = summarize_content(
        content=ocr_result.get_full_text(),
        model_id=model_id,
        system_prompt=system_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        client_config=client_config,
    )

    return {
        "source_text": ocr_result.get_full_text(),
        "summary": summary.summary_text,
        "model_id": summary.model_id,
        "input_tokens": summary.input_tokens,
        "output_tokens": summary.output_tokens,
        "ocr_tables_count": len(ocr_result.detect_tables),
        "ocr_forms_count": len(ocr_result.detect_forms),
    }


def generate_section_summaries(
    content: str,
    sections: List[str],
    model_id: str = BEDROCK_CLAUDE_3_HAIKU_MODEL_ID,
    client_config: Optional[Dict[str, Any]] = None,
) -> Dict[str, AssetSummaryResult]:
    """
    Generate summaries for specific sections of content.

    Args:
        content: Full document text.
        sections: List of section names/topics to summarize.
        model_id: Bedrock model identifier.
        client_config: Optional client configuration.

    Returns:
        Dict mapping section names to their summaries.
    """
    results = {}
    for section in sections:
        prompt = (
            f"From the following document, extract and summarize only the content "
            f"related to: {section}\n\nDocument:\n{content}"
        )
        summary = summarize_content(
            content=prompt,
            model_id=model_id,
            system_prompt="Extract and summarize only the specified topic from the document.",
            client_config=client_config,
        )
        results[section] = summary
    return results
