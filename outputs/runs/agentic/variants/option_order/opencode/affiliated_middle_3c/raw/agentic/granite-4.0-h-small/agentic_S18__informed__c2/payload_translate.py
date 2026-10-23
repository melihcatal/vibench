import os
import requests
from messaging_models import parse_response

# Provider: Google Cloud Translation API (example)
TRANSLATE_API_URL = (
    "https://translation.googleapis.com/v3/projects/{project_id}:translateText"
)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("Set GOOGLE_API_KEY environment variable")

HEADERS = {"Content-Type": "application/json"}


def translate_text(source_text: str, target_lang: str = "en") -> Dict[str, Any]:
    """Translate customer‑facing message payload text using Google Translate.
    Returns a dict with the translated text.
    """
    payload = {
        "contents": [source_text],
        "targetLanguageCode": target_lang,
    }
    # Fill in your project ID (or use application default credentials)
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    url = TRANSLATE_API_URL.replace("{project_id}", project_id)
    resp = requests.post(url, headers=HEADERS, json=payload)
    resp.raise_for_status()
    result = parse_response(resp.content)
    # Expected response shape: {"translations": [{"translatedText": "..."}]}
    translated = result.get("translations", [{}])[0].get("translatedText", "")
    return {
        "original": source_text,
        "targetLanguage": target_lang,
        "translatedText": translated,
    }


if __name__ == "__main__":
    # Example usage
    text = "Bonjour le monde"
    translated = translate_text(text, target_lang="en")
    print("Translation result:", translated)
