import json
import os

from google import genai

from model_client import build_model_config, build_prompt, get_api_key
from model_models import normalize_json_output


def extract_json(payload, config=None):
    config = build_model_config(config)
    prompt = build_prompt(
        "Extract structured JSON from the text. Return only valid JSON matching the requested schema.",
        payload.get("text", ""),
    )
    schema = payload.get("schema")
    if schema:
        prompt += "\n\nSchema:\n" + json.dumps(schema, ensure_ascii=False)
    with genai.Client(api_key=get_api_key(config, "GOOGLE_API_KEY")) as client:
        response = client.models.generate_content(model=config["model"], contents=prompt)
    return normalize_json_output(response.text or "")
