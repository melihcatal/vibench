from google import genai


client = genai.Client()


def appeal_translate(text: str, target_language: str) -> str:
    prompt = f"Translate the following appeal text into {target_language}: {text}"
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    return getattr(response, "text", "") or ""
