import json
from typing import Dict, Any

from model_client import get_llm_client
from model_models import LLMRequest, LLMResponse


def extract_json(
    text: str,
    schema: Dict[str, Any],
    model_family: str = "qwen",
    model_id: str = "qwen-plus",
    max_tokens: int = 500,
    temperature: float = 0.3,
) -> Dict[str, Any]:
    """
    Extract structured JSON from text using DashScope Qwen API.
    """
    client = get_llm_client()

    schema_str = json.dumps(schema, indent=2)
    prompt = (
        f"Extract structured data from the following text based on the provided JSON schema. "
        f"Ensure the output is valid JSON and adheres to the schema:\n\n"
        f"Schema: {schema_str}\n\n"
        f"Text: {text}\n\n"
        f"Output:"
    )

    request = LLMRequest(
        model_family=model_family,
        model_id=model_id,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    response: LLMResponse = client.generate(request)

    # Parse the response text to extract JSON
    try:
        json_start = response.text.find("{")
        json_end = response.text.rfind("}") + 1
        json_str = response.text[json_start:json_end]
        return json.loads(json_str)
    except (json.JSONDecodeError, ValueError) as e:
        raise ValueError(f"Failed to parse JSON from response: {e}")
