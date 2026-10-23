import requests
from observability_client import get_translator_url, get_auth_header


def log_message_translate(message: str, target_locale: str = "es") -> str:
    """Translate a support‑visible log message to another locale.

    Calls the provider's translation API (e.g., Azure Translator Text API) with
    the raw log string and returns the translated text. The provider URL and
    auth header are fetched from the helper module.
    """
    url = get_translator_url()
    headers = {
        **get_auth_header(),
        "Content-Type": "application/json",
        "Accept-Language": target_locale,
    }
    payload = {
        "text": message,
        "to": target_locale,
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        # Expected response shape: {"translatedText": "..."}
        return result.get("translatedText", message)
    except requests.RequestException as e:
        print(f"Translation request failed: {e}")
        return message


if __name__ == "__main__":
    example = "An error occurred while processing request 12345."
    translated = log_message_translate(example, target_locale="fr")
    print("Original:", example)
    print("Translated (French):", translated)
