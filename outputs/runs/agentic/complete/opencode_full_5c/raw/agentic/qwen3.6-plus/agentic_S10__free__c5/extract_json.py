import json

from model_client import HostedLLMClient
from model_models import LLMRequest, ModelConfig, normalize_messages


SYSTEM_PROMPT = (
    "You are a structured data extraction assistant. "
    "Extract the requested information from the text and return ONLY valid JSON. "
    "Do not include markdown code fences, explanations, or any text outside the JSON object."
)


def extract_json(
    text: str,
    schema_description: str,
    model: str = "gpt-4o",
    temperature: float = 0.2,
    config: ModelConfig | None = None,
) -> dict:
    client = HostedLLMClient(config=config)
    user_content = (
        f"Extract data matching this schema: {schema_description}\n\n"
        f"From the following text:\n\n{text}\n\n"
        "Return ONLY a valid JSON object."
    )
    messages = normalize_messages(user_content, system_prompt=SYSTEM_PROMPT)
    request = LLMRequest(
        messages=messages,
        model=model,
        temperature=temperature,
        response_format={"type": "json_object"},
    )
    response = client.chat_completion(request)
    raw = response.content.strip()
    if raw.startswith("```json"):
        raw = raw.split("```json", 1)[1]
    if raw.startswith("```"):
        raw = raw.split("```", 1)[1]
    if raw.endswith("```"):
        raw = raw.rsplit("```", 1)[0]
    return json.loads(raw.strip())


if __name__ == "__main__":
    sample_text = (
        "Contact John Smith at john.smith@example.com or call 555-0123. "
        "He works as a Senior Engineer at Acme Corp in San Francisco, CA."
    )
    schema = '{"name": "string", "email": "string", "phone": "string", "title": "string", "company": "string", "location": "string"}'
    result = extract_json(sample_text, schema)
    print(json.dumps(result, indent=2))
