"""
Summarize content extracted from a stored asset using OpenAI GPT-4o-mini.

Downloads and extracts text from a stored object, then uses the
OpenAI Chat Completions API (gpt-4o-mini model) to generate summaries.
"""

import os
import json
from typing import Optional, List, Dict, Any

import boto3
from openai import OpenAI
from openai.types.chat import ChatCompletion

from storage_client import get_s3_client, get_bucket_name
from stored_document_ocr import run_ocr_on_stored_document, OcrResult
from object_metadata import get_object_metadata

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")
OPENAI_MAX_TOKENS = int(os.environ.get("OPENAI_SUMMARY_MAX_TOKENS", "1024"))
OPENAI_TEMPERATURE = float(os.environ.get("OPENAI_SUMMARY_TEMPERATURE", "0.3"))


class AssetSummary:
    """Generated summary of an asset's content."""

    def __init__(
        self,
        summary: str,
        key_points: Optional[List[str]] = None,
        word_count: int = 0,
        source_bucket: Optional[str] = None,
        source_key: Optional[str] = None,
        model_used: str = OPENAI_MODEL,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.summary = summary
        self.key_points = key_points or []
        self.word_count = word_count
        self.source_bucket = source_bucket
        self.source_key = source_key
        self.model_used = model_used
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary": self.summary,
            "key_points": self.key_points,
            "word_count": self.word_count,
            "source_bucket": self.source_bucket,
            "source_key": self.source_key,
            "model_used": self.model_used,
            "metadata": self.metadata,
        }


def _get_openai_client() -> OpenAI:
    """Create and return an OpenAI client."""
    # Provider signal: openai.OpenAI (OpenAI API)
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=OPENAI_API_KEY)


def _download_object_text(key: str, bucket: Optional[str] = None, s3_client=None) -> str:
    """
    Download and extract text from an S3 object.
    Attempts OCR for image/PDF files, reads plain text for text files.
    """
    bucket_name = get_bucket_name(bucket)
    client = s3_client or get_s3_client()

    metadata = get_object_metadata(key=key, bucket=bucket_name, s3_client=client)
    if not metadata.exists:
        raise FileNotFoundError(f"Object not found: s3://{bucket_name}/{key}")

    content_type = metadata.content_type or ""

    # For text-based content types, download directly
    if any(ct in content_type for ct in ["text/", "application/json", "application/xml"]):
        response = client.get_object(Bucket=bucket_name, Key=key)
        return response["Body"].read().decode("utf-8", errors="replace")

    # For documents and images, run OCR
    ocr_result = run_ocr_on_stored_document(key=key, bucket=bucket_name, s3_client=client)
    return ocr_result.full_text


def summarize_asset_content(
    key: str,
    bucket: Optional[str] = None,
    summary_type: str = "general",
    max_length: int = OPENAI_MAX_TOKENS,
    temperature: float = OPENAI_TEMPERATURE,
    custom_prompt: Optional[str] = None,
    include_key_points: bool = True,
    s3_client=None,
    openai_client=None,
) -> AssetSummary:
    """
    Generate a summary of content extracted from a stored asset.

    Args:
        key: S3 object key of the asset
        bucket: S3 bucket name
        summary_type: Type of summary (general, executive, technical, etc.)
        max_length: Maximum tokens for the summary
        temperature: Sampling temperature for generation
        custom_prompt: Custom summarization prompt
        include_key_points: Whether to extract key points
        s3_client: Pre-configured boto3 S3 client
        openai_client: Pre-configured OpenAI client

    Returns:
        AssetSummary with generated summary and key points
    """
    bucket_name = get_bucket_name(bucket)
    client = s3_client or get_s3_client()
    ai_client = openai_client or _get_openai_client()

    # Download and extract text from the stored object
    extracted_text = _download_object_text(key=key, bucket=bucket_name, s3_client=client)

    if not extracted_text or not extracted_text.strip():
        return AssetSummary(
            summary="No extractable text content found in the asset.",
            source_bucket=bucket_name,
            source_key=key,
            model_used=OPENAI_MODEL,
        )

    # Build the summarization prompt
    if custom_prompt:
        system_prompt = custom_prompt
    else:
        system_prompt = (
            f"You are an expert document analyst. Provide a {summary_type} summary of the following content. "
            f"Be concise, accurate, and capture the main ideas. "
            f"Focus on the most important information and context."
        )

    if include_key_points:
        system_prompt += (
            "\n\nAlso extract 3-7 key points as a bulleted list."
            "\nFormat your response as JSON with keys: 'summary' (string) and 'key_points' (list of strings)."
        )

    # Truncate text if too long for the model context
    # gpt-4o-mini has 128k context, but we limit to ~30k tokens for safety
    max_chars = 100000
    truncated_text = extracted_text[:max_chars]
    if len(extracted_text) > max_chars:
        truncated_text += "\n\n[Content truncated due to length]"

    user_message = f"Content to summarize:\n\n{truncated_text}"

    try:
        # Call OpenAI Chat Completions API with gpt-4o-mini model
        # Provider signal: openai.ChatCompletion with model="gpt-4o-mini"
        response: ChatCompletion = ai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            max_tokens=max_length,
            temperature=temperature,
            response_format={"type": "json_object"} if include_key_points else None,
        )

        assistant_message = response.choices[0].message.content or ""

        if include_key_points:
            try:
                parsed = json.loads(assistant_message)
                summary_text = parsed.get("summary", assistant_message)
                key_points = parsed.get("key_points", [])
            except json.JSONDecodeError:
                summary_text = assistant_message
                key_points = []
        else:
            summary_text = assistant_message
            key_points = []

        word_count = len(summary_text.split())

        # Get object metadata for additional context
        obj_metadata = get_object_metadata(key=key, bucket=bucket_name, s3_client=client)

        return AssetSummary(
            summary=summary_text,
            key_points=key_points,
            word_count=word_count,
            source_bucket=bucket_name,
            source_key=key,
            model_used="gpt-4o-mini",
            metadata={
                "content_type": obj_metadata.content_type,
                "content_length": obj_metadata.content_length,
                "last_modified": obj_metadata.last_modified.isoformat() if obj_metadata.last_modified else None,
            },
        )

    except Exception as e:
        raise RuntimeError(f"OpenAI gpt-4o-mini summarization failed: {e}") from e


def batch_summarize_assets(
    keys: List[str],
    bucket: Optional[str] = None,
    summary_type: str = "general",
    s3_client=None,
) -> List[AssetSummary]:
    """
    Summarize multiple stored assets.

    Args:
        keys: List of S3 object keys
        bucket: S3 bucket name
        summary_type: Type of summary
        s3_client: Pre-configured boto3 S3 client

    Returns:
        List of AssetSummary objects
    """
    return [
        summarize_asset_content(
            key=k,
            bucket=bucket,
            summary_type=summary_type,
            s3_client=s3_client,
        )
        for k in keys
    ]
