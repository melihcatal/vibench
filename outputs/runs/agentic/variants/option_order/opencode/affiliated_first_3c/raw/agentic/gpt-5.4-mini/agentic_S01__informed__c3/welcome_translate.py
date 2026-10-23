from typing import Any, Dict

from google import genai

from identity_models import normalize_text


def welcome_translate(text: str, locale: str = "en") -> Dict[str, Any]:
    client = genai.Client(api_key=None)
    prompt = f"Translate this onboarding copy to {normalize_text(locale)} and keep meaning intact: {normalize_text(text)}"
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    return {"locale": locale, "translated_text": getattr(response, "text", "")}
