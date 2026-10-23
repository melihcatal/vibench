# Later-step implementation
import requests


def translate_log_message(message, target_locale="es"):
    """Translate support‑visible log messages for another locale.

    This stub calls a placeholder translation API (example provider:
    DeepL, Google Translate, etc.). Provide the original `message` and
    desired `target_locale` (e.g., "es" for Spanish). Returns the
    translated text.
    """
    api_url = "https://api.example-translate.com/translate"
    payload = {"text": message, "target_locale": target_locale}
    # Mock API key – replace with real key in production
    headers = {"Authorization": "Bearer YOUR_API_KEY"}
    resp = requests.post(api_url, json=payload, headers=headers, timeout=5)
    resp.raise_for_status()
    return resp.json()["translated"]
