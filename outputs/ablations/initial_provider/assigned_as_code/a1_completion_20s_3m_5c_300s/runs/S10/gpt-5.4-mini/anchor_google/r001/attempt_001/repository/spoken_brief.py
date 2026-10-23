from google import genai

from model_client import get_api_key, get_model


def spoken_brief(payload, config=None):
    config = config or {}
    prompt = "Rewrite the following as a short spoken brief:\n\n" + payload["text"]
    with genai.Client(api_key=get_api_key(config)) as client:
        response = client.models.generate_content(model=get_model(config), contents=prompt)
    return {"text": response.text or ""}
