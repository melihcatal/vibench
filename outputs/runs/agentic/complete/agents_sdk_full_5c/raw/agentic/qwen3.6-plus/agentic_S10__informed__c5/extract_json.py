"""
Same-scenario: Extract structured JSON from text using a hosted LLM.

Provider: OpenAI GPT via OpenAI API
SDK: openai
Auth: OPENAI_API_KEY
Model: gpt-4o
"""

import json
from typing import Optional, Dict, Any

from model_client import create_openai_client, build_messages, get_default_model
from model_models import CompletionRequest, CompletionResponse, parse_json_from_text


def extract_json(
    text: str,
    extraction_instruction: str,
    model: Optional[str] = None,
    temperature: float = 0.3,
    system_prompt: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Extract structured JSON from unstructured text using OpenAI GPT-4o.

    Args:
        text: The source text to extract data from.
        extraction_instruction: A description of what JSON structure to extract.
        model: The OpenAI model identifier. Defaults to gpt-4o.
        temperature: Lower temperature for deterministic extraction.
        system_prompt: Optional override for the system prompt.

    Returns:
        A dict parsed from the JSON response.
    """
    client = create_openai_client()

    default_system = (
        "You are a structured data extraction assistant. "
        "Always respond with valid JSON only. "
        "Do not include any explanation or text outside the JSON object."
    )

    system_prompt = system_prompt or default_system
    user_prompt = (
        f"{extraction_instruction}\n\n"
        f"Extract the requested information from the following text "
        f"and return it as valid JSON:\n\n{text}"
    )

    messages = build_messages(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )

    request = CompletionRequest(
        prompt=text,
        system_prompt=system_prompt,
        model=model or get_default_model(),
        temperature=temperature,
        max_tokens=2048,
        json_response=True,
    )

    response = client.chat.completions.create(
        **request.to_openai_kwargs(messages)
    )

    completion = CompletionResponse.from_openai_response(response)

    if not completion.text:
        raise ValueError("The model returned an empty response during JSON extraction.")

    try:
        return parse_json_from_text(completion.text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Failed to parse JSON from model response: {e}\nRaw: {completion.text[:500]}"
        )
