from google import genai


DEFAULT_MODEL = "gemini-2.0-flash"


def moderation_summary(decisions, api_key=None, model=DEFAULT_MODEL):
    client = genai.Client(api_key=api_key)
    prompt = f"Summarize these moderation decisions concisely: {decisions}"
    response = client.models.generate_content(model=model, contents=prompt)
    return {"summary": getattr(response, "text", ""), "model": model}
