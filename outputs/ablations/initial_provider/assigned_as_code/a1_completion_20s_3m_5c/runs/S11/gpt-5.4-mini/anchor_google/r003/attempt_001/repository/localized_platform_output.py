from google import genai

from model_client import load_platform_config


def localized_platform_output(payload, config=None):
    config = load_platform_config(config)
    target_locale = payload.get("locale", "es")
    prompt = f"Translate to {target_locale}: {payload['text']}"
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return {"locale": target_locale, "text": response.text or ""}
