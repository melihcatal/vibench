import json

from model_client import get_client, get_model_config
from model_models import normalize_json_output


def extract_json(text: str) -> dict:
    client = get_client()
    config = get_model_config()
    prompt = f"Extract the key information from the text and return only valid JSON:\n\n{text}"
    response = client.models.generate_content(
        model=config.model,
        contents=prompt,
        config={
            "temperature": 0.0,
            "top_p": 1.0,
            "max_output_tokens": config.max_output_tokens,
            "response_mime_type": "application/json",
        },
    )
    return json.loads(normalize_json_output(getattr(response, "text", response)))
