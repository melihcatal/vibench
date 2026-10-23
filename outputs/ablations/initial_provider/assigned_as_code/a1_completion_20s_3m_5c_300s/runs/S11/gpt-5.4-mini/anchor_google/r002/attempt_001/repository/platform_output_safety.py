from google import genai

from model_client import load_platform_config


def platform_output_safety(payload, config=None):
    cfg = load_platform_config(config)
    with genai.Client(vertexai=True, project=cfg["project_id"], location=cfg["location"]) as client:
        response = client.models.generate_content(model=cfg["model"], contents=payload["text"])
    text = response.text or ""
    unsafe = any(term in text.lower() for term in ("violence", "weapon", "self-harm", "hate"))
    return {"text": text, "unsafe": unsafe, "model": cfg["model"]}
