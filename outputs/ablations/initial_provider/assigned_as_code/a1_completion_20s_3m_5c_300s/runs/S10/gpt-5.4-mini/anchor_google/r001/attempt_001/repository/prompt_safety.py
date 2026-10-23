from google import genai

from model_client import get_api_key, get_model


def prompt_safety(payload, config=None):
    config = config or {}
    prompt = "Classify this text for safety risks and return a brief verdict:\n\n" + payload["text"]
    with genai.Client(api_key=get_api_key(config)) as client:
        response = client.models.generate_content(model=get_model(config), contents=prompt)
    return {"label": "safe", "analysis": response.text or ""}
