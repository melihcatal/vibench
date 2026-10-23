import os, requests

BASE_URL = "https://api.translatorprovider.com/v1"  # concrete translation provider
API_KEY = os.getenv("TRANSLATOR_API_KEY")

def translate_welcome(user_locale: str, message: str) -> str:
    """Translate onboarding copy into the user's locale using provider API."""
    payload = {
        "source": "en",
        "target": user_locale,
        "text": message,
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(f"{BASE_URL}/translate", json=payload, headers=headers)
    response.raise_for_status()
    result = response.json()
    return result["translatedText"]
