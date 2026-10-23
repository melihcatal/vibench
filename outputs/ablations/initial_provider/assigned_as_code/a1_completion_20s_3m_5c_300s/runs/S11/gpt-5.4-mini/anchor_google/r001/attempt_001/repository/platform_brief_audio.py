from google import genai


def platform_brief_audio(payload, config=None):
    config = config or {}
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        response = client.models.generate_content(model=payload.get("model", "gemini-2.5-flash"), contents=f"Create a spoken briefing for: {payload['text']}")
    return {"audio_brief": response.text or "", "response": response}
