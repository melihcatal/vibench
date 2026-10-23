"""
extract_json.py - Calls a hosted OpenAI LLM to extract structured JSON from text.

Uses the OpenAI Chat Completions API with JSON response format for structured extraction.
"""

import json

from model_client import get_openai_client, select_model, build_chat_messages
from model_models import LLMRequest, LLMResponse, normalize_json_response, build_extraction_request


def extract_json(
    text: str,
    schema_description: str,
    model_family: str = "gpt-4o",
    temperature: float = 0.2,
) -> dict:
    """
    Extract structured JSON from the provided text using OpenAI's hosted LLM.

    Args:
        text: The text to extract information from.
        schema_description: Description of the JSON schema to extract.
        model_family: OpenAI model family to use (e.g. "gpt-4o").
        temperature: Sampling temperature (kept low for deterministic extraction).

    Returns:
        Parsed dictionary extracted from the text.
    """
    request = build_extraction_request(text, schema_description, model_family)
    request.temperature = temperature

    client = get_openai_client()
    model_id = select_model(request.model_family)

    messages = build_chat_messages(
        system_prompt=request.system_prompt,
        user_content=request.user_content,
        format_instructions="Return ONLY valid JSON. No explanations, no markdown code fences.",
    )

    params = request.to_openai_params(model=model_id, messages=messages)

    completion = client.chat.completions.create(**params)

    content = ""
    if completion.choices and completion.choices[0].message:
        content = completion.choices[0].message.content or ""

    extracted = normalize_json_response(content)
    return extracted


def extract_json_with_response(
    text: str,
    schema_description: str,
    model_family: str = "gpt-4o",
    temperature: float = 0.2,
) -> LLMResponse:
    """
    Extract structured JSON and return the full LLMResponse with metadata.

    Args:
        text: The text to extract information from.
        schema_description: Description of the JSON schema.
        model_family: OpenAI model family.
        temperature: Sampling temperature.

    Returns:
        LLMResponse with extracted JSON as text and usage metadata.
    """
    request = build_extraction_request(text, schema_description, model_family)
    request.temperature = temperature

    client = get_openai_client()
    model_id = select_model(request.model_family)

    messages = build_chat_messages(
        system_prompt=request.system_prompt,
        user_content=request.user_content,
        format_instructions="Return ONLY valid JSON. No explanations, no markdown code fences.",
    )

    params = request.to_openai_params(model=model_id, messages=messages)

    completion = client.chat.completions.create(**params)

    content = ""
    if completion.choices and completion.choices[0].message:
        content = completion.choices[0].message.content or ""

    usage = completion.usage
    return LLMResponse(
        text=content,
        model_used=model_id,
        prompt_tokens=usage.prompt_tokens if usage else 0,
        completion_tokens=usage.completion_tokens if usage else 0,
        total_tokens=usage.total_tokens if usage else 0,
        finish_reason=completion.choices[0].finish_reason if completion.choices else "",
        raw_response=completion,
    )


if __name__ == "__main__":
    sample = (
        "John Smith works as a Senior Software Engineer at Acme Corp in San Francisco. "
        "He has been with the company since January 2020 and earns $145,000 annually. "
        "His email is john.smith@acmecorp.com and he manages a team of 6 developers."
    )
    schema = (
        "Extract: name (string), title (string), company (string), "
        "location (string), start_date (string), salary (number), "
        "email (string), team_size (integer)"
    )
    result = extract_json(sample, schema, model_family="gpt-4o")
    print(json.dumps(result, indent=2))
