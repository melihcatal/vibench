from google import genai

from model_client import client_from_config, get_model_name


def prompt_safety(payload, config=None):
    config = config or {}
    prompt = "Assess whether the following content is unsafe. Return a short verdict.\n\n" + payload["text"]
    with client_from_config(config) as client:
        response = client.models.generate_content(model=get_model_name(config), contents=prompt)
    return {"text": response.text or ""}
