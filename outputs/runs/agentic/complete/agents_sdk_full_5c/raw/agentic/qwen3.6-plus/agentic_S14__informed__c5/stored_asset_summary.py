"""
stored_asset_summary.py - Summarize content extracted from a stored asset.

Uses OpenAI API via openai SDK with gpt-4o model as the concrete hosted LLM inference provider.
Authentication via OPENAI_API_KEY environment variable.
"""

import os
from typing import Optional, List
from openai import OpenAI


def summarize_extracted_content(
    extracted_text: str,
    model: str = "gpt-4o",
    max_tokens: int = 500,
    temperature: float = 0.3,
    api_key: Optional[str] = None,
    system_prompt: Optional[str] = None,
) -> str:
    """
    Summarize extracted text content using OpenAI GPT-4o model.

    Args:
        extracted_text: The text content to summarize (e.g., from OCR or document extraction).
        model: OpenAI model identifier (default: gpt-4o).
        max_tokens: Maximum tokens for the summary response.
        temperature: Sampling temperature (lower = more deterministic).
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.
        system_prompt: Optional custom system prompt.

    Returns:
        Generated summary text.

    Raises:
        ValueError: If extracted_text is empty.
        RuntimeError: If the summarization request fails.
    """
    if not extracted_text or not extracted_text.strip():
        raise ValueError("extracted_text is required and cannot be empty.")

    openai_api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError(
            "OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key."
        )

    client = OpenAI(api_key=openai_api_key)

    default_system = (
        "You are an expert document summarization assistant. "
        "Provide a concise, accurate summary of the provided text. "
        "Focus on key points, main themes, and important details. "
        "Keep the summary clear and well-structured."
    )

    system_message = system_prompt or default_system

    # Truncate very long inputs to fit within context limits
    max_input_chars = 100000
    if len(extracted_text) > max_input_chars:
        extracted_text = extracted_text[:max_input_chars] + "...[truncated]"

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"Please summarize the following document:\n\n{extracted_text}"},
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        summary = response.choices[0].message.content
        return summary

    except Exception as e:
        raise RuntimeError(f"OpenAI GPT-4o summarization failed: {e}") from e


def summarize_with_custom_instructions(
    extracted_text: str,
    instructions: str,
    model: str = "gpt-4o",
    max_tokens: int = 500,
    temperature: float = 0.3,
    api_key: Optional[str] = None,
) -> str:
    """
    Summarize text with custom instructions using OpenAI GPT-4o.

    Args:
        extracted_text: The text content to process.
        instructions: Specific instructions for how to summarize or process the text.
        model: OpenAI model identifier.
        max_tokens: Maximum tokens for response.
        temperature: Sampling temperature.
        api_key: OpenAI API key.

    Returns:
        Generated text based on instructions.
    """
    if not extracted_text or not extracted_text.strip():
        raise ValueError("extracted_text is required.")
    if not instructions or not instructions.strip():
        raise ValueError("instructions are required.")

    openai_api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OpenAI API key is required.")

    client = OpenAI(api_key=openai_api_key)

    max_input_chars = 100000
    if len(extracted_text) > max_input_chars:
        extracted_text = extracted_text[:max_input_chars] + "...[truncated]"

    messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": extracted_text},
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content

    except Exception as e:
        raise RuntimeError(f"OpenAI GPT-4o custom summarization failed: {e}") from e


def extract_key_entities(
    extracted_text: str,
    model: str = "gpt-4o",
    api_key: Optional[str] = None,
) -> List[dict]:
    """
    Extract key entities (people, organizations, dates, amounts) from text using GPT-4o.

    Args:
        extracted_text: Text to extract entities from.
        model: OpenAI model identifier.
        api_key: OpenAI API key.

    Returns:
        List of extracted entity dicts with type and value.
    """
    openai_api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OpenAI API key is required.")

    client = OpenAI(api_key=openai_api_key)

    system_prompt = (
        "Extract key entities from the provided text. Return a JSON array of objects "
        "with keys: 'type' (person, organization, date, amount, location, other), "
        "'value' (the extracted value), and 'context' (brief context). "
        "Only return the JSON array, nothing else."
    )

    max_input_chars = 50000
    if len(extracted_text) > max_input_chars:
        extracted_text = extracted_text[:max_input_chars]

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": extracted_text},
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=1000,
            temperature=0.1,
        )
        return response.choices[0].message.content

    except Exception as e:
        raise RuntimeError(f"OpenAI GPT-4o entity extraction failed: {e}") from e
