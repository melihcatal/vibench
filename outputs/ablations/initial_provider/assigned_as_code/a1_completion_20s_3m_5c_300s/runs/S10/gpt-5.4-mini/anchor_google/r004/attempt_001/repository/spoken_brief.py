import os

from google import genai

from model_client import build_model_config, get_api_key


def spoken_brief(payload, config=None):
    config = build_model_config(config)
    prompt = "Rewrite the following model output as a brief spoken summary suitable for audio narration.\n\n" + payload.get("text", "")
    with genai.Client(api_key=get_api_key(config, "GOOGLE_API_KEY")) as client:
        response = client.models.generate_content(model=config["model"], contents=prompt)
    return {"text": response.text or ""}
