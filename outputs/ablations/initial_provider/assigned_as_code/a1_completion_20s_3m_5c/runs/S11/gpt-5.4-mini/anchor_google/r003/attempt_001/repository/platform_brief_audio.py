from google import genai

from model_client import load_platform_config


def platform_brief_audio(payload, config=None):
    config = load_platform_config(config)
    brief = payload["text"]
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=f"Write a short spoken briefing: {brief}")
    return {"text": response.text or ""}
