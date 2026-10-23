"""
Summarize content extracted from a stored asset using Anthropic Claude via the Messages API.

Uses the Anthropic Python SDK (anthropic) to call the Claude model family
(e.g., claude-3-sonnet-20240229, claude-3-haiku-20240307) for content
summarization. Authentication via ANTHROPIC_API_KEY environment variable.
"""

from __future__ import annotations

import logging
import os
from typing import Optional

import anthropic

logger = logging.getLogger(__name__)

# Provider-identifying environment variable for Anthropic
ANTHROPIC_API_KEY_ENV = "ANTHROPIC_API_KEY"

# Anthropic Claude model identifiers
CLAUDE_MODEL_SONNET = "claude-3-sonnet-20240229"
CLAUDE_MODEL_HAIKU = "claude-3-haiku-20240307"
CLAUDE_MODEL_OPUS = "claude-3-opus-20240229"
CLAUDE_MODEL_SONNET_35 = "claude-3-5-sonnet-20240620"

DEFAULT_CLAUDE_MODEL = CLAUDE_MODEL_SONNET


def create_anthropic_client(
    api_key: Optional[str] = None,
) -> anthropic.Anthropic:
    """
    Create an Anthropic API client using the Python SDK.

    Args:
        api_key: Anthropic API key. Falls back to ANTHROPIC_API_KEY env var.

    Returns:
        Configured anthropic.Anthropic client instance.
    """
    key = api_key or os.environ.get(ANTHROPIC_API_KEY_ENV)
    if not key:
        raise ValueError(
            f"Anthropic API key not provided. Set the {ANTHROPIC_API_KEY_ENV} environment variable."
        )
    client = anthropic.Anthropic(api_key=key)
    logger.debug("Created Anthropic client for model family: Claude")
    return client


def summarize_content(
    content: str,
    *,
    model: str = DEFAULT_CLAUDE_MODEL,
    max_tokens: int = 1024,
    temperature: float = 0.3,
    summary_type: str = "brief",
    api_key: Optional[str] = None,
    client: Optional[anthropic.Anthropic] = None,
) -> str:
    """
    Generate a summary of the provided content using Anthropic Claude.

    Args:
        content: The text content to summarize.
        model: Anthropic Claude model ID to use.
        max_tokens: Maximum tokens in the response.
        temperature: Sampling temperature (lower = more deterministic).
        summary_type: 'brief', 'detailed', or 'executive'.
        api_key: Optional Anthropic API key.
        client: Optional pre-created anthropic.Anthropic client.

    Returns:
        Summarized text string.
    """
    if client is None:
        client = create_anthropic_client(api_key=api_key)

    summary_instructions = {
        "brief": (
            "Provide a concise summary (2-3 sentences) of the following content. "
            "Focus on the key points and main ideas only."
        ),
        "detailed": (
            "Provide a comprehensive summary of the following content. "
            "Include all important details, key arguments, and supporting points. "
            "Structure the summary with clear paragraphs."
        ),
        "executive": (
            "Provide an executive summary of the following content. "
            "Include key findings, recommendations, and action items if applicable. "
            "Format with bullet points for readability."
        ),
    }

    instruction = summary_instructions.get(summary_type, summary_instructions["brief"])

    system_prompt = (
        "You are a helpful document summarization assistant. "
        "Your task is to accurately summarize the content provided."
    )

    user_message = f"{instruction}\n\n---\nContent to summarize:\n{content}"

    try:
        message = client.messages.create(
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
    except anthropic.APIError as exc:
        logger.error("Anthropic Claude summarization failed: %s", exc)
        raise

    summary = ""
    for block in message.content:
        if block.type == "text":
            summary += block.text

    logger.info(
        "Summarized content using Anthropic %s (%d input chars -> %d output chars)",
        model,
        len(content),
        len(summary),
    )
    return summary


def summarize_asset_content(
    asset_text: str,
    asset_metadata: Optional[dict] = None,
    *,
    model: str = DEFAULT_CLAUDE_MODEL,
    api_key: Optional[str] = None,
    client: Optional[anthropic.Anthropic] = None,
) -> dict:
    """
    Generate a structured summary of asset content using Anthropic Claude.

    Returns a dict with summary, key_topics, sentiment, and content_type.

    Args:
        asset_text: Extracted text from the stored asset.
        asset_metadata: Optional metadata about the asset (filename, size, etc.).
        model: Anthropic Claude model ID.
        api_key: Optional Anthropic API key.
        client: Optional pre-created anthropic.Anthropic client.

    Returns:
        Dict with 'summary', 'key_topics', 'sentiment', and 'content_type'.
    """
    if client is None:
        client = create_anthropic_client(api_key=api_key)

    metadata_info = ""
    if asset_metadata:
        metadata_parts = [f"{k}: {v}" for k, v in asset_metadata.items()]
        metadata_info = f"Asset metadata: {', '.join(metadata_parts)}.\n"

    system_prompt = (
        "You are an asset analysis assistant. Analyze the provided content and "
        "return a JSON object with these fields: "
        '"summary" (2-3 sentence summary), '
        '"key_topics" (list of 3-5 main topics), '
        '"sentiment" (positive, neutral, or negative), '
        '"content_type" (classification like report, article, contract, etc.). '
        "Respond ONLY with valid JSON, no markdown or extra text."
    )

    user_message = (
        f"{metadata_info}"
        f"Analyze the following asset content:\n\n{asset_text}"
    )

    try:
        message = client.messages.create(
            model=model,
            max_tokens=1024,
            temperature=0.2,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
        )
    except anthropic.APIError as exc:
        logger.error("Anthropic Claude asset analysis failed: %s", exc)
        raise

    result_text = ""
    for block in message.content:
        if block.type == "text":
            result_text += block.text

    import json

    try:
        # Try to parse as JSON
        result = json.loads(result_text.strip())
    except json.JSONDecodeError:
        # Fall back to returning raw text as summary
        result = {
            "summary": result_text.strip(),
            "key_topics": [],
            "sentiment": "unknown",
            "content_type": "unknown",
        }

    logger.info(
        "Analyzed asset using Anthropic %s: topics=%s, sentiment=%s",
        model,
        result.get("key_topics"),
        result.get("sentiment"),
    )
    return result
