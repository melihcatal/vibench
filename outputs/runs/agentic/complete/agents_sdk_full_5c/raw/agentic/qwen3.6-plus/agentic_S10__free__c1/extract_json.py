"""
extract_json.py — calls a hosted LLM (OpenAI gpt-4o) to extract structured
JSON from arbitrary text.

Uses the OpenAI Chat Completions API (api.openai.com) with JSON mode
enabled on the gpt-4o-2024-08-06 model.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from model_client import run_completion, resolve_model
from model_models import build_chat_request, CompletionResponse, parse_json_response

# Concrete OpenAI model identifier for JSON extraction
EXTRACTION_MODEL = resolve_model("gpt-4o")  # gpt-4o-2024-08-06

EXTRACTION_SYSTEM_PROMPT = (
    "You are a structured-data extraction assistant. "
    "Extract the requested information from the user's text and return "
    "only a valid JSON object. Do not include markdown fences or any "
    "explanatory text. The JSON should match the schema described by the user."
)


def extract_json(
    text: str,
    schema_description: str,
    model: Optional[str] = None,
    temperature: float = 0.2,
    max_tokens: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Extract structured JSON from text using the hosted OpenAI gpt-4o model.

    Parameters
    ----------
    text : str
        Source text containing the data to extract.
    schema_description : str
        Natural-language description of the expected JSON structure.
    model : str, optional
        Concrete OpenAI model ID (defaults to gpt-4o-2024-08-06).
    temperature : float
        Sampling temperature (kept low for deterministic extraction).
    max_tokens : int, optional
        Maximum output tokens.

    Returns
    -------
    dict
        Parsed JSON object extracted from the text.
    """
    target_model = model or EXTRACTION_MODEL
    user_prompt = (
        f"Extract information according to this schema: {schema_description}\n\n"
        f"Source text:\n{text}"
    )
    request = build_chat_request(
        system_prompt=EXTRACTION_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        model=target_model,
        temperature=temperature,
        max_tokens=max_tokens,
        json_mode=True,
    )
    response: CompletionResponse = run_completion(request)
    return parse_json_response(response.content)


if __name__ == "__main__":
    sample = (
        "Contact John Smith at john.smith@example.com or call (555) 123-4567. "
        "He works at Acme Corp in San Francisco as a Senior Engineer."
    )
    schema = (
        '{"name": "string", "email": "string", "phone": "string", '
        '"company": "string", "location": "string", "title": "string"}'
    )
    result = extract_json(sample, schema)
    print("Extracted JSON:")
    import json
    print(json.dumps(result, indent=2))
