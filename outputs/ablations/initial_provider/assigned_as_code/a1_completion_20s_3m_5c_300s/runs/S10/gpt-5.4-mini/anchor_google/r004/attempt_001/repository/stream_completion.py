import os

from google import genai

from model_client import build_model_config, build_prompt, get_api_key


def stream_completion(payload, config=None):
    config = build_model_config(config)
    prompt = build_prompt(payload.get("instruction", "Continue the text."), payload.get("text", ""))
    chunks = []
    with genai.Client(api_key=get_api_key(config, "GOOGLE_API_KEY")) as client:
        for chunk in client.models.generate_content_stream(model=config["model"], contents=prompt):
            text = getattr(chunk, "text", "") or ""
            if text:
                chunks.append(text)
    return {"text": "".join(chunks)}
