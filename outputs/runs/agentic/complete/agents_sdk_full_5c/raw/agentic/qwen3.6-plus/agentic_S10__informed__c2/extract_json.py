"""
Extract structured JSON from text using a hosted LLM.

Provider: OpenAI Chat Completions API
SDK: openai
Auth: OPENAI_API_KEY
Concrete model: gpt-4o
Endpoint: api.openai.com/v1/chat/completions
"""

import json
from typing import Any, Dict, Optional

from model_client import call_llm_sync
from model_models import (
    LLMRequest,
    LLMResponse,
    build_json_extraction_request,
)


def extract_json(
    text: str,
    schema_description: str,
    model_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Extract structured JSON from text using the OpenAI gpt-4o model.

    Args:
        text: The input text to extract data from.
        schema_description: A description of the expected JSON schema.
        model_name: Optional model override (default: gpt-4o).

    Returns:
        A dictionary containing the extracted JSON data.

    Raises:
        ValueError: If the model output is not valid JSON.
    """
    effective_model = model_name or "gpt-4o"
    request = build_json_extraction_request(
        text=text,
        schema_description=schema_description,
        model_name=effective_model,
    )
    response = call_llm_sync(request)

    content = response.content.strip()
    # Remove markdown code fences if present
    if content.startswith("```json"):
        content = content[7:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Failed to parse JSON from OpenAI gpt-4o response: {e}\n"
            f"Raw response: {response.content}"
        ) from e


def extract_json_custom(
    text: str,
    system_prompt: str,
    model_name: str = "gpt-4o",
    temperature: float = 0.1,
) -> Dict[str, Any]:
    """
    Extract JSON from text using a custom system prompt via OpenAI.

    Args:
        text: The input text.
        system_prompt: Custom system prompt for JSON extraction.
        model_name: OpenAI model identifier.
        temperature: Sampling temperature.

    Returns:
        Extracted JSON as a dictionary.
    """
    request = LLMRequest(
        user_prompt=text,
        system_prompt=system_prompt,
        model_name=model_name,
        temperature=temperature,
        max_tokens=2048,
        json_mode=True,
    )
    response = call_llm_sync(request)

    content = response.content.strip()
    if content.startswith("```json"):
        content = content[7:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Failed to parse JSON from OpenAI response: {e}"
        ) from e
