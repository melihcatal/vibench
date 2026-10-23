from google import genai


DEFAULT_MODEL = "gemini-2.0-flash"


def appeal_translate(text, target_language, api_key=None, model=DEFAULT_MODEL):
    client = genai.Client(api_key=api_key)
    prompt = f"Translate this moderation appeal into {target_language}: {text}"
    response = client.models.generate_content(model=model, contents=prompt)
    return {"translation": getattr(response, "text", ""), "model": model}
