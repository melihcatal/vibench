from google import genai

from model_client import get_api_key, get_model


def result_translate(payload, config=None):
    config = config or {}
    target_language = payload.get("target_language", "English")
    prompt = "Translate the following text into " + target_language + ":\n\n" + payload["text"]
    with genai.Client(api_key=get_api_key(config)) as client:
        response = client.models.generate_content(model=get_model(config), contents=prompt)
    return {"text": response.text or ""}
