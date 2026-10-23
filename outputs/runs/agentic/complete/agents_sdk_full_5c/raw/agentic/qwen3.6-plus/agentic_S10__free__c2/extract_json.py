"""
Extract structured JSON from text using a hosted LLM.
Provider: OpenAI - https://platform.openai.com
Model: gpt-4o (openai-gpt4o family) with JSON mode response_format
"""

from typing import Optional, Dict, Any
from model_client import get_openai_client, resolve_model_family, DEFAULT_EXTRACT_MODEL
from model_models import (
    LLMRequest,
    LLMResponse,
    normalize_system_user_messages,
    parse_json_from_text,
)


EXTRACT_SYSTEM_PROMPT = (
    "You are a structured data extraction assistant. Your task is to extract "
    "information from the provided text and return it as a valid JSON object. "
    "Only output valid JSON with no additional text or markdown formatting."
)


def extract_json(
    text: str,
    extraction_schema: Optional[Dict[str, Any]] = None,
    model: str = DEFAULT_EXTRACT_MODEL,
    temperature: float = 0.0,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> LLMResponse:
    """
    Send text to the OpenAI gpt-4o model at api.openai.com and extract structured JSON.

    Uses OpenAI's json_object response_format to enforce valid JSON output.

    Args:
        text: The text content to extract data from.
        extraction_schema: Optional JSON schema to guide extraction via OpenAI structured outputs.
        model: OpenAI model identifier (default: gpt-4o).
        temperature: Sampling temperature (0.0 recommended for extraction).
        api_key: Optional override for OPENAI_API_KEY env variable.
        base_url: Optional override for OpenAI API endpoint.

    Returns:
        LLMResponse with the raw extracted JSON text.
    """
    response_format = {"type": "json_object"}

    messages = normalize_system_user_messages(
        EXTRACT_SYSTEM_PROMPT,
        f"Extract structured data from the following text:\n\n{text}",
    )

    request = LLMRequest(
        model=model,
        messages=messages,
        temperature=temperature,
        response_format=response_format,
    )

    client = get_openai_client(api_key=api_key, base_url=base_url)
    openai_kwargs = request.to_openai_kwargs()
    response = client.chat.completions.create(**openai_kwargs)

    return LLMResponse.from_openai(response, model=model)


def extract_json_typed(
    text: str,
    instructions: str,
    model: str = DEFAULT_EXTRACT_MODEL,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Extract typed JSON from text using OpenAI gpt-4o and return parsed dict.

    Args:
        text: The source text.
        instructions: Specific extraction instructions describing the expected fields.
        model: OpenAI model identifier.
        api_key: Optional API key override.
        base_url: Optional base URL override.

    Returns:
        Parsed dictionary from the LLM's JSON response.
    """
    system_prompt = (
        f"{EXTRACT_SYSTEM_PROMPT}\n\n"
        f"Extraction instructions: {instructions}"
    )

    result = extract_json(
        text=text,
        model=model,
        api_key=api_key,
        base_url=base_url,
    )
    result.messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Extract structured data from the following text:\n\n{text}"},
    ]

    return parse_json_from_text(result.text)


if __name__ == "__main__":
    sample = (
        "Contact: Jane Doe, Email: jane@example.com, Phone: 555-0199. "
        "She works at Acme Corp as a Senior Engineer and joined in March 2020."
    )
    result = extract_json(
        text=sample,
        instructions="Extract: name, email, phone, company, title, join_date"
    )
    print(f"Model family: {resolve_model_family(result.model)}")
    print(f"Extracted JSON: {result.text}")
    parsed = parse_json_from_text(result.text)
    print(f"Parsed: {parsed}")
