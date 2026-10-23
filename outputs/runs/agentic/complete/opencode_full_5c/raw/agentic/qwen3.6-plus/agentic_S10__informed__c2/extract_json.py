import json
from typing import Any, Optional

from model_client import execute_llm_request, select_model_for_task
from model_models import LLMRequest, LLMResponse, build_system_prompt, truncate_text


def extract_json(
    text: str,
    schema_description: str = "Extract all relevant structured data as JSON.",
    model: str = "gpt-4o",
    temperature: float = 0.1,
) -> dict[str, Any]:
    truncated = truncate_text(text, max_chars=80000)
    system = build_system_prompt(
        task_description="You are a data extraction specialist. Extract structured information from the given text and return it as valid JSON.",
        output_format="A single valid JSON object with no markdown formatting or code fences.",
        constraints=[
            "Return ONLY valid JSON, nothing else",
            "Do not include markdown code fences or backticks",
            f"Schema guidance: {schema_description}",
            "Use null for missing or unknown values",
        ],
    )
    request = LLMRequest(
        model=model or select_model_for_task("extraction", require_json=True),
        system_prompt=system,
        user_prompt=f"Extract structured JSON from the following text:\n\n{truncated}",
        temperature=temperature,
        max_tokens=4096,
        json_mode=True,
    )
    response = execute_llm_request(request)
    return _parse_json_response(response.content)


def _parse_json_response(content: str) -> dict[str, Any]:
    cleaned = content.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[len("```json") :]
    if cleaned.startswith("```"):
        cleaned = cleaned[len("```") :]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()
    return json.loads(cleaned)


def extract_entities(
    text: str,
    entity_types: Optional[list[str]] = None,
    model: str = "gpt-4o",
) -> dict[str, Any]:
    types = entity_types or ["person", "organization", "location", "date", "event"]
    schema = f"Extract entities of these types: {', '.join(types)}. Group them by type in a JSON object."
    return extract_json(text, schema_description=schema, model=model)


def extract_key_values(
    text: str,
    keys: list[str],
    model: str = "gpt-4o",
) -> dict[str, Any]:
    schema = (
        f"Extract the following key-value pairs as a JSON object: {', '.join(keys)}."
    )
    return extract_json(text, schema_description=schema, model=model)
