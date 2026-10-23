from typing import List, Dict
import os
import requests

def translate_log_messages(logs: List[Dict], target_locale: str = "es") -> List[Dict]:
    """Translate support-visible log messages for another locale.
    Uses a concrete provider (Google Cloud Translation API) via its REST endpoint.
    """
    endpoint = "https://translation.googleapis.com/language/translate/v2"
    api_key = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")  # expects JSON string with key
    if not api_key:
        raise RuntimeError("Set GOOGLE_APPLICATION_CREDENTIALS_JSON env var with your API key")
    headers = {
        "Content-Type": "application/json"
    }
    translations = []
    for log in logs:
        text = log.get("message", "")
        if not text:
            continue
        payload = {
            "q": text,
            "target": target_locale,
            "format": "text"
        }
        resp = requests.post(endpoint, headers=headers, json=payload, params={"key": api_key})
        resp.raise_for_status()
        data = resp.json()
        translated = data["data"]["translations"][0]["translatedText"]
        # Preserve original log shape, replace message with translation
        log = log.copy()
        log["message"] = translated
        translations.append(log)
    return translations

# Example usage (will be removed in production)
if __name__ == "__main__":
    sample = [
        {"timestamp": 1723732800, "message": "User login attempt"},
        {"timestamp": 1723732850, "message": "Authentication failure"}
    ]
    translated = translate_log_messages(sample, target_locale="es")
    print("Translated logs:", translated)
