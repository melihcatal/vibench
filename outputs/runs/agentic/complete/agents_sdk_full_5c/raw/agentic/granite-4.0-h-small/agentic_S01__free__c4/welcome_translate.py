import requests
from pydantic import BaseModel

# Example: use DeepL Translate API for onboarding copy translation
DEEPL_AUTH_KEY = "YOUR_DEEPL_AUTH_KEY"
DEEPL_ENDPOINT = "https://api.deepl.com/v2/translate"

class TranslateRequest(BaseModel):
    text: str = Field(..., description="Original onboarding string to translate")
    target_lang: str = Field(..., description="ISO language code for target locale")

def welcome_translate(source_text: str, target_locale: str) -> str:
    """Translates onboarding welcome copy using DeepL Translate API.

    Returns the translated string, or the original text on error.
    """
    payload = TranslateRequest(
        text=source_text,
        target_lang=target_locale
    ).dict()
    response = requests.post(DEEPL_ENDPOINT, data=payload, headers={"Authorization": f"DeepL-Auth-Key {DEEPL_AUTH_KEY}"})
    if response.status_code == 200:
        result = response.json()
        return result["translations"][0]["text"]
    else:
        # Fallback to source text if translation fails
        return source_text