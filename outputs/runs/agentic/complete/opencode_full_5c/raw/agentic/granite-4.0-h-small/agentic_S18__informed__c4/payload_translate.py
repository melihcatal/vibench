import requests
from messaging_models import TranslatedText

# Example: Google Cloud Translation REST endpoint
TRANSLATE_URL = "https://translation.googleapis.com/v3/projects/{}/locations/{}/translations:translate"
API_KEY = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")  # or use header auth

HEADERS = {"Authorization": f"Bearer {API_KEY}"}


def translate(text: str, target_lang: str) -> TranslatedText:
    """Translate arbitrary text using the configured provider."""
    payload = {"source_text": text, "target_language_code": target_lang}
    response = requests.post(
        TRANSLATE_URL.format(
            os.getenv("GOOGLE_PROJECT_ID"), os.getenv("GOOGLE_LOCATION", "global")
        ),
        headers=HEADERS,
        json=payload,
    )
    data = response.json()
    translated = data.get("translated_text", "")
    return TranslatedText(target=target_lang, translated=translated)
