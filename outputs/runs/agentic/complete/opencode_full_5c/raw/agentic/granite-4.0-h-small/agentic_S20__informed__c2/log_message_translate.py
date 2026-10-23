import os
import json
import requests
from observability_client import init_datadog_session, get_datadog_api_key
from observability_models import NormalizedLog

# Provider: DeepL Translation API (example)


def translate_log(log: NormalizedLog, target_locale: str = "ja") -> NormalizedLog:
    url = "https://api.deepl.com/v2/translate"
    params = {
        "auth_key": os.getenv("DEEPL_AUTH_KEY"),
        "text": log.message,
        "target_lang": target_locale,
    }
    response = requests.post(url, params=params)
    if response.status_code != 200:
        raise RuntimeError(f"Translation API error: {response.text}")
    result = response.json()
    translated_text = result.get("translations", [{}])[0].get("text")
    # Return a copy with translated message
    translated_log = dataclasses.replace(log, message=translated_text)
    return translated_log


# Example usage (remove in production)
if __name__ == "__main__":
    original = NormalizedLog(
        timestamp=datetime.datetime.utcnow(),
        level="INFO",
        message="Feature flag enabled",
    )
    translated = translate_log(original, target_locale="es")
    print("Translated log:", translated.to_dict())
