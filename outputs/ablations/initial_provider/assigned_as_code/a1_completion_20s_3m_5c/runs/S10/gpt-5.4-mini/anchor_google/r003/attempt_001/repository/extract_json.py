from google import genai

from model_client import client_from_config, get_model_name


def extract_json(payload, config=None):
    config = config or {}
    prompt = "Extract the requested information as valid JSON only.\n\n" + payload["text"]
    with client_from_config(config) as client:
        response = client.models.generate_content(model=get_model_name(config), contents=prompt)
    return {"json": response.text or ""}
