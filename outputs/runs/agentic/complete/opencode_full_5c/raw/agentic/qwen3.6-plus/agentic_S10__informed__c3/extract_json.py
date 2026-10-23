import json
from typing import Optional
from model_client import create_chat_completion, get_openai_client
from model_models import LLMRequest, LLMResponse


def extract_json(
    text: str,
    schema_description: str = "a JSON object with key-value pairs",
    model: str = "gpt-4o",
    api_key: Optional[str] = None,
) -> dict:
    client = get_openai_client(api_key) if api_key else None
    request = LLMRequest(
        prompt=text,
        model=model,
        temperature=0.1,
        max_tokens=1024,
        json_mode=True,
        system_prompt=(
            "Extract structured information from the following text and return it as valid JSON. "
            f"The output should be {schema_description}. "
            "Return ONLY the JSON object with no markdown formatting or explanation."
        ),
    )
    response = create_chat_completion(request, client)
    raw = response.text.strip()
    if raw.startswith("```"):
        first_nl = raw.index("\n")
        last_backtick = raw.rindex("```")
        raw = raw[first_nl:last_backtick].strip()
    return json.loads(raw)
