import os
from google import genai


def welcome_translate(text: str, locale: str) -> str:
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    model = "gemini-2.0-flash"
    prompt = f"Translate the onboarding copy into {locale}. Return only the translated text. Copy: {text}"
    response = client.models.generate_content(model=model, contents=prompt)
    return response.text or ""
