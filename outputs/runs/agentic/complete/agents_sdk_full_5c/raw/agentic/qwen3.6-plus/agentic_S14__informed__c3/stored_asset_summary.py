"""
Summarize content extracted from a stored asset using Anthropic Claude.

Uses anthropic SDK for Anthropic Messages API (service=Anthropic Messages API).
Model: claude-3-sonnet-20240229 (with claude-3-haiku-20240307 and claude-3-opus-20240229 as alternatives).
Environment variable: ANTHROPIC_API_KEY
"""

from typing import Dict, List, Optional

import anthropic

from stored_document_ocr import run_ocr_on_stored_document


DEFAULT_MODEL = "claude-3-sonnet-20240229"

SUPPORTED_MODELS = [
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
    "claude-3-opus-20240229",
    "claude-3-5-sonnet-20240620",
]


def _get_anthropic_client() -> anthropic.Anthropic:
    """
    Create an Anthropic API client using the ANTHROPIC_API_KEY environment variable.

    Returns:
        anthropic.Anthropic: Authenticated client for Anthropic Messages API.

    Raises:
        ValueError: If ANTHROPIC_API_KEY is not set.
    """
    import os

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY environment variable must be set for Anthropic API access"
        )
    return anthropic.Anthropic(api_key=api_key)


def _build_system_prompt(summary_type: str, detail_level: str) -> str:
    """
    Build a system prompt for the summarization task.

    Args:
        summary_type: Type of summary ("general", "key_points", "executive", "technical").
        detail_level: Level of detail ("brief", "medium", "comprehensive").

    Returns:
        str: System prompt string for Claude.
    """
    type_prompts = {
        "general": "Provide a clear, general summary of the document content.",
        "key_points": "Extract and list the key points and main takeaways from the document.",
        "executive": "Provide an executive summary suitable for business decision-makers.",
        "technical": "Provide a technical summary focusing on specifications, processes, and technical details.",
    }

    detail_prompts = {
        "brief": "Keep the summary concise and brief.",
        "medium": "Provide a moderately detailed summary.",
        "comprehensive": "Provide a thorough, comprehensive summary covering all important aspects.",
    }

    system = type_prompts.get(summary_type, type_prompts["general"])
    system += " " + detail_prompts.get(detail_level, detail_prompts["medium"])

    return system


def summarize_stored_asset(
    bucket: str,
    object_key: str,
    prefix: Optional[str] = None,
    summary_type: str = "general",
    detail_level: str = "medium",
    model: str = DEFAULT_MODEL,
    max_tokens: int = 2048,
    temperature: float = 0.3,
) -> Dict:
    """
    Summarize the text content extracted from a stored S3 document using Anthropic Claude.

    Runs OCR on the stored document, then sends the extracted text to Claude
    for summarization via the Messages API.

    Args:
        bucket: The S3 bucket containing the document.
        object_key: The S3 object key of the document.
        prefix: Optional prefix for the S3 object key.
        summary_type: Type of summary ("general", "key_points", "executive", "technical").
        detail_level: Level of detail ("brief", "medium", "comprehensive").
        model: Anthropic Claude model identifier (default: claude-3-sonnet-20240229).
        max_tokens: Maximum tokens in the response (default: 2048).
        temperature: Sampling temperature (default: 0.3).

    Returns:
        dict with keys:
            - summary: The generated summary text
            - model: The Claude model used
            - original_text_length: Length of the original extracted text
            - summary_type: The type of summary requested
            - detail_level: The detail level requested
            - usage: Token usage information from the API

    Raises:
        FileNotFoundError: If the S3 object does not exist.
        anthropic.APIError: On Anthropic API errors.
    """
    if model not in SUPPORTED_MODELS:
        model = DEFAULT_MODEL

    ocr_result = run_ocr_on_stored_document(bucket, object_key, prefix=prefix)
    extracted_text = ocr_result["text"]

    if not extracted_text.strip():
        return {
            "summary": "No text content could be extracted from the document.",
            "model": model,
            "original_text_length": 0,
            "summary_type": summary_type,
            "detail_level": detail_level,
            "usage": {},
        }

    system_prompt = _build_system_prompt(summary_type, detail_level)

    user_message = (
        f"Please summarize the following document content.\n\n"
        f"<document>\n{extracted_text}\n</document>"
    )

    client = _get_anthropic_client()

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": user_message,
            }
        ],
    )

    summary_text = ""
    for content_block in response.content:
        if content_block.type == "text":
            summary_text += content_block.text

    return {
        "summary": summary_text.strip(),
        "model": model,
        "original_text_length": len(extracted_text),
        "summary_type": summary_type,
        "detail_level": detail_level,
        "usage": {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        },
    }


def summarize_text_direct(
    text: str,
    summary_type: str = "general",
    detail_level: str = "medium",
    model: str = DEFAULT_MODEL,
    max_tokens: int = 2048,
    temperature: float = 0.3,
) -> Dict:
    """
    Summarize text directly without OCR (for already-extracted text).

    Args:
        text: The text content to summarize.
        summary_type: Type of summary.
        detail_level: Level of detail.
        model: Anthropic Claude model identifier.
        max_tokens: Maximum tokens in the response.
        temperature: Sampling temperature.

    Returns:
        dict with summary and metadata.
    """
    system_prompt = _build_system_prompt(summary_type, detail_level)

    user_message = (
        f"Please summarize the following document content.\n\n"
        f"<document>\n{text}\n</document>"
    )

    client = _get_anthropic_client()

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": user_message,
            }
        ],
    )

    summary_text = ""
    for content_block in response.content:
        if content_block.type == "text":
            summary_text += content_block.text

    return {
        "summary": summary_text.strip(),
        "model": model,
        "original_text_length": len(text),
        "summary_type": summary_type,
        "detail_level": detail_level,
        "usage": {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        },
    }
