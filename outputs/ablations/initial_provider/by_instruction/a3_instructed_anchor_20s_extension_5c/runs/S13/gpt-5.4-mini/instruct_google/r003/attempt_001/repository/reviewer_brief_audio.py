from google import genai


DEFAULT_MODEL = "gemini-2.0-flash"


def reviewer_brief_audio(text, api_key=None, model=DEFAULT_MODEL):
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model=model, contents=f"Create a spoken moderation brief for: {text}")
    return {"brief": getattr(response, "text", ""), "model": model}
