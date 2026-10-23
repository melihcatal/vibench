from __future__ import annotations

import json
from typing import Any, Optional

from model_client import call_llm
from model_models import (
    LLMRequest,
    LLMResponse,
    extract_json_from_text,
    normalize_prompt,
)

EXTRACTOR_MODEL = "gpt-4o-mini"
EXTRACTOR_SYSTEM_PROMPT = (
    "You are a structured data extraction assistant. Extract the requested information "
    "from the provided text and return ONLY valid JSON. Do not include markdown code fences, "
    "explanations, or any text outside the JSON object."
)


def extract_json(
    text: str,
    schema_description: str = "Extract all key entities, facts, and relationships as a JSON object.",
    temperature: float = 0.1,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> dict[str, Any]:
    normalized = normalize_prompt(text)
    prompt = (
        f"{schema_description}\n\n"
        f"Extract structured JSON from the following text:\n\n"
        f"{normalized}"
    )
    request = LLMRequest(
        model=model or EXTRACTOR_MODEL,
        prompt=prompt,
        system_prompt=EXTRACTOR_SYSTEM_PROMPT,
        temperature=temperature,
        max_tokens=4096,
        json_mode=True,
    )
    response = call_llm(request, api_key=api_key, base_url=base_url)
    parsed = extract_json_from_text(response.text)
    if parsed is not None:
        return parsed
    return {"raw_extraction": response.text, "parse_error": True}


def extract_json_with_schema(
    text: str,
    json_schema: dict[str, Any],
    temperature: float = 0.1,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> dict[str, Any]:
    normalized = normalize_prompt(text)
    schema_str = json.dumps(json_schema, indent=2)
    prompt = (
        f"Extract data from the following text according to this JSON schema:\n\n"
        f"Schema: {schema_str}\n\n"
        f"Text to extract from:\n\n"
        f"{normalized}"
    )
    request = LLMRequest(
        model=model or EXTRACTOR_MODEL,
        prompt=prompt,
        system_prompt=EXTRACTOR_SYSTEM_PROMPT,
        temperature=temperature,
        max_tokens=4096,
        json_mode=True,
    )
    response = call_llm(request, api_key=api_key, base_url=base_url)
    parsed = extract_json_from_text(response.text)
    if parsed is not None:
        return parsed
    return {"raw_extraction": response.text, "parse_error": True}


if __name__ == "__main__":
    import os

    result = extract_json(
        text="John Smith, age 35, works as a software engineer at Acme Corp in San Francisco...",
        schema_description="Extract person name, age, job title, company, and location.",
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    print(json.dumps(result, indent=2))
