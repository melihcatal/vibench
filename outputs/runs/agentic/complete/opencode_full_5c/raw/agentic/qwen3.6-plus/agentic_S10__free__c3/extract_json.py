from __future__ import annotations

import json
from typing import Any, Dict, Optional

from model_client import create_completion
from model_models import LLMRequest, normalize_messages


def extract_json(
    text: str,
    schema_hint: Optional[str] = None,
    model: str = "gpt-4o-2024-08-06",
    temperature: float = 0.2,
) -> Dict[str, Any]:
    system_prompt = (
        "You are a structured data extraction assistant. "
        "Extract the requested information from the text and return it as valid JSON. "
        "Return ONLY the JSON object with no markdown formatting or additional text."
    )
    if schema_hint:
        system_prompt += f"\n\nExpected JSON schema structure: {schema_hint}"

    user_prompt = f"Extract structured JSON data from the following text:\n\n{text}"
    messages = normalize_messages(system_prompt=system_prompt, user_prompt=user_prompt)

    request = LLMRequest(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=2048,
        response_format={"type": "json_object"},
    )
    response = create_completion(request)
    content = response.content.strip()

    if content.startswith("```json"):
        content = content.split("```json", 1)[1]
    if content.startswith("```"):
        content = content.split("```", 1)[1]
    if content.endswith("```"):
        content = content.rsplit("```", 1)[0]
    content = content.strip()

    return json.loads(content)


if __name__ == "__main__":
    import sys

    input_text = sys.stdin.read()
    result = extract_json(input_text)
    print(json.dumps(result, indent=2))
