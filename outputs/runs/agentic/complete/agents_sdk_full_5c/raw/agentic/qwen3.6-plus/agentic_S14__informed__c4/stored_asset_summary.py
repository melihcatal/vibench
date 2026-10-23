"""
stored_asset_summary.py — Summarize content extracted from a stored asset.

Concrete provider: Anthropic Messages API via the `anthropic` SDK.
Provider signals:
  - anthropic import and Anthropic client
  - claude-3-sonnet-20240229 model identifier
  - ANTHROPIC_API_KEY environment variable
"""

import os
from typing import Dict, Optional
from anthropic import Anthropic, APIStatusError


def summarize_stored_asset_content(
    extracted_text: str,
    model: str = "claude-3-sonnet-20240229",
    max_tokens: int = 1024,
    summary_style: str = "concise",
    language: str = "en",
) -> Dict:
    """
    Summarize extracted text content from a stored document/asset
    using Anthropic Claude via the Messages API.

    Parameters
    ----------
    extracted_text : str
        Text content extracted from the stored asset (e.g., OCR output).
    model : str
        Anthropic Claude model identifier (default: claude-3-sonnet-20240229).
    max_tokens : int
        Maximum tokens for the summary response.
    summary_style : str
        Style hint for the summary: "concise", "detailed", or "executive".
    language : str
        Language for the summary output (ISO 639-1).

    Returns
    -------
    dict
        Normalized summary result with the generated text and metadata.

    Raises
    ------
    APIStatusError
        When the Anthropic API returns an error status.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = Anthropic(api_key=api_key)

    style_instructions = {
        "concise": "Provide a brief, concise summary in 3-5 sentences.",
        "detailed": "Provide a thorough, detailed summary covering all key points.",
        "executive": "Provide an executive summary with key findings, recommendations, and actionable items.",
    }.get(summary_style, "Provide a summary of the content.")

    system_prompt = (
        f"You are a document analysis assistant. {style_instructions} "
        f"Write the summary in {language}."
    )

    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Please summarize the following extracted document content:\n\n{extracted_text}",
                    }
                ],
            }
        ],
    )

    summary_text = ""
    for block in message.content:
        if block.type == "text":
            summary_text += block.text

    return {
        "summary": summary_text,
        "model": model,
        "service": "Anthropic Messages API",
        "summary_style": summary_style,
        "language": language,
        "input_tokens": message.usage.input_tokens,
        "output_tokens": message.usage.output_tokens,
        "stop_reason": message.stop_reason,
    }


def summarize_asset_with_metadata(
    extracted_text: str,
    asset_metadata: Optional[Dict] = None,
    model: str = "claude-3-haiku-20240307",
    max_tokens: int = 512,
) -> Dict:
    """
    Summarize asset content along with its metadata for richer context.

    Parameters
    ----------
    extracted_text : str
        Extracted text from the asset.
    asset_metadata : dict, optional
        Object metadata (e.g., filename, content type, size, custom tags).
    model : str
        Anthropic model to use (default: claude-3-haiku-20240307).
    max_tokens : int
        Maximum response tokens.

    Returns
    -------
    dict
        Summary result including metadata-aware analysis.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = Anthropic(api_key=api_key)

    metadata_str = ""
    if asset_metadata:
        metadata_str = "\n\nAsset metadata:\n" + "\n".join(
            f"  {k}: {v}" for k, v in asset_metadata.items()
        )

    system_prompt = (
        "You are a document intelligence assistant. Summarize the provided asset "
        "content and its metadata. Include document type, key topics, and notable entities."
    )

    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Summarize this document content:{metadata_str}\n\nExtracted text:\n{extracted_text}",
                    }
                ],
            }
        ],
    )

    summary_text = ""
    for block in message.content:
        if block.type == "text":
            summary_text += block.text

    return {
        "summary": summary_text,
        "model": model,
        "service": "Anthropic Messages API",
        "input_tokens": message.usage.input_tokens,
        "output_tokens": message.usage.output_tokens,
        "stop_reason": message.stop_reason,
        "metadata_included": asset_metadata is not None,
    }
