import json
from typing import Any

from model_models import ModelRequest, ModelResponse
from model_client import create_chat_completion


def extract_json(
    text: str, schema_hint: str = "", model: str = "gpt-4o"
) -> dict[str, Any]:
    system_prompt = (
        "You are a structured data extraction assistant. "
        "Extract the requested information from the text and return ONLY valid JSON. "
        "Do not include any explanatory text, markdown formatting, or code fences. "
        "Return a single JSON object."
    )

    prompt = text
    if schema_hint:
        prompt = f"Extract data matching this schema:\n{schema_hint}\n\nText to extract from:\n{text}"

    request = ModelRequest(
        prompt=prompt,
        system_prompt=system_prompt,
        model=model,
        temperature=0.1,
        max_tokens=2048,
        json_mode=True,
    )

    response = create_chat_completion(request, default_system=system_prompt)

    raw_text = response.text.strip()
    if raw_text.startswith("```json"):
        raw_text = raw_text[7:]
    if raw_text.startswith("```"):
        raw_text = raw_text[3:]
    if raw_text.endswith("```"):
        raw_text = raw_text[:-3]
    raw_text = raw_text.strip()

    return json.loads(raw_text)


if __name__ == "__main__":
    import sys

    input_text = sys.stdin.read()
    result = extract_json(input_text)
    print(json.dumps(result, indent=2))
