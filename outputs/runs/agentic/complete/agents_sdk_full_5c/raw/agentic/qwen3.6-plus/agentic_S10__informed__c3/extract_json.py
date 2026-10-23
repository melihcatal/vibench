"""
Extract structured JSON from text using the Mistral AI hosted LLM.

Provider: Mistral AI Chat API
SDK: mistralai
Auth: MISTRAL_API_KEY
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional

from model_client import build_request, create_mistral_client, execute_chat
from model_models import (
    LLMResponse,
    LLMRequest,
    build_json_extraction_prompt,
)


def extract_json(
    text: str,
    schema: Optional[Dict[str, Any]] = None,
    model: Optional[str] = None,
    temperature: float = 0.1,
) -> Dict[str, Any]:
    """Extract structured JSON from arbitrary text using a Mistral AI model.

    Args:
        text: The text to extract structured data from.
        schema: Optional JSON schema to guide the extraction.
        model: Optional concrete Mistral model identifier (e.g., 'mistral-large-latest').
        temperature: Sampling temperature kept low for deterministic JSON output.

    Returns:
        Parsed dictionary extracted from the text.
    """
    prompt = build_json_extraction_prompt(text, schema=schema)

    system_prompt = (
        "You are a structured data extraction assistant. Always return valid JSON "
        "only, with no markdown code fences or surrounding text."
    )

    request = build_request(
        prompt=prompt,
        system_prompt=system_prompt,
        model=model,
        max_tokens=2048,
        temperature=temperature,
    )

    response = execute_chat(request)
    return parse_json_response(response.content)


def extract_json_with_client(
    text: str,
    client,
    schema: Optional[Dict[str, Any]] = None,
    model: Optional[str] = None,
    temperature: float = 0.1,
) -> Dict[str, Any]:
    """Extract structured JSON using a pre-created Mistral client.

    Args:
        text: The text to extract structured data from.
        client: An initialized mistralai.Mistral client.
        schema: Optional JSON schema to guide extraction.
        model: Optional concrete Mistral model identifier.
        temperature: Sampling temperature.

    Returns:
        Parsed dictionary extracted from the text.
    """
    prompt = build_json_extraction_prompt(text, schema=schema)

    system_prompt = (
        "You are a structured data extraction assistant. Always return valid JSON "
        "only, with no markdown code fences or surrounding text."
    )

    request = build_request(
        prompt=prompt,
        system_prompt=system_prompt,
        model=model,
        max_tokens=2048,
        temperature=temperature,
    )

    response = execute_chat(request, client=client)
    return parse_json_response(response.content)


def parse_json_response(content: str) -> Dict[str, Any]:
    """Parse JSON from an LLM response string, stripping markdown fences if present."""
    cleaned = content.strip()

    # Strip markdown code fences if present
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        # Remove opening fence line
        if lines[0].startswith("```"):
            lines = lines[1:]
        # Remove closing fence line
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()

    # Try to find JSON object boundaries
    first_brace = cleaned.find("{")
    last_brace = cleaned.rfind("}")
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        cleaned = cleaned[first_brace : last_brace + 1]

    return json.loads(cleaned)
