from google import genai


def localized_platform_output(payload, config=None):
    config = config or {}
    target_locale = config.get("locale", "es")
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        response = client.models.generate_content(model=config.get("model", "gemini-2.5-flash"), contents=f"Translate to {target_locale}: {payload['text']}")
    return {"locale": target_locale, "text": response.text or "", "response": response}
