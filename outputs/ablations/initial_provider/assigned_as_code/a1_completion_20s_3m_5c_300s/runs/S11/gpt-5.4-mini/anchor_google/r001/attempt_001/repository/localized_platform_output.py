from google import genai


def localized_platform_output(payload, config=None):
    config = config or {}
    target_locale = payload.get("locale", "es")
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        response = client.models.generate_content(model=payload.get("model", "gemini-2.5-flash"), contents=f"Translate to {target_locale}: {payload['text']}")
    return {"text": response.text or "", "locale": target_locale, "response": response}
