from google import genai

from model_client import load_platform_config


def localized_platform_output(payload, config=None):
    cfg = load_platform_config(config)
    target_locale = payload.get("locale") or cfg["locale"]
    prompt = f"Translate the following text to {target_locale}: {payload['text']}"
    with genai.Client(vertexai=True, project=cfg["project_id"], location=cfg["location"]) as client:
        response = client.models.generate_content(model=cfg["model"], contents=prompt)
    return {"text": response.text or "", "locale": target_locale, "model": cfg["model"]}
