import os

from google import genai

from model_client import build_model_config, get_api_key


def result_translate(payload, config=None):
    config = build_model_config(config)
    target_language = payload.get("language", "English")
    text = payload.get("text", "")
    prompt = f"Translate the following text into {target_language}:\n\n{text}"
    with genai.Client(api_key=get_api_key(config, "GOOGLE_API_KEY")) as client:
        response = client.models.generate_content(model=config["model"], contents=prompt)
    return {"text": response.text or ""}
