import os

from google import genai

from model_client import build_model_config, get_api_key


def prompt_safety(payload, config=None):
    config = build_model_config(config)
    prompt = payload.get("text", "")
    instruction = "Classify whether the following text contains unsafe content. Return SAFE or UNSAFE with a short reason."
    with genai.Client(api_key=get_api_key(config, "GOOGLE_API_KEY")) as client:
        response = client.models.generate_content(model=config["model"], contents=instruction + "\n\n" + prompt)
    text = response.text or ""
    unsafe = "unsafe" in text.lower()
    return {"safe": not unsafe, "text": text}
