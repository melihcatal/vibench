import json
from model_client import create_openai_client, execute_completion
from model_models import LLMRequest, normalize_messages

OPENAI_JSON_EXTRACTION_MODEL = "gpt-4o"
OPENAI_API_HOST = "api.openai.com"


def extract_json(
    text: str,
    schema_description: str = "Extract all key-value pairs as a JSON object.",
    temperature: float = 0.1,
    api_key: str | None = None,
) -> dict:
    client = create_openai_client(api_key=api_key)
    system_prompt = (
        "You are a structured data extraction assistant. "
        "Extract information from the provided text and return ONLY valid JSON. "
        f"{schema_description} "
        "Do not include markdown code fences or any explanatory text."
    )
    messages = normalize_messages(system_prompt=system_prompt, user_content=text)
    request = LLMRequest(
        model=OPENAI_JSON_EXTRACTION_MODEL,
        messages=messages,
        temperature=temperature,
        response_format={"type": "json_object"},
    )
    response = execute_completion(client, request)
    content = response.content.strip()
    if content.startswith("```json"):
        content = content.split("```json", 1)[1]
        if "```" in content:
            content = content.rsplit("```", 1)[0]
        content = content.strip()
    elif content.startswith("```"):
        content = content.split("```", 1)[1]
        if "```" in content:
            content = content.rsplit("```", 1)[0]
        content = content.strip()
    return json.loads(content)
