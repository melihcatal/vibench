import requests
from observability_client import get_aws_credentials

# Example using Google Cloud Translation API (could be swapped for other providers)


def translate_dashboard_notes(notes, target_locale="fr"):
    """Translate metric or dashboard notes for another locale using Google Cloud Translation API.

    Parameters:
        notes (dict): Dictionary where keys are note IDs and values are note texts.
        target_locale (str): Locale code (e.g., 'fr' for French).

    Returns:
        dict: Translated notes mapping ID to translated text.
    """
    url = "https://translation.googleapis.com/language/translate/v2"
    api_key = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS"
    )  # assumes credentials file is configured
    headers = {"Content-Type": "application/json"}
    payload = {"q": list(notes.values()), "target": target_locale, "format": "text"}
    resp = requests.post(url, headers=headers, params={"key": api_key}, json=payload)
    resp.raise_for_status()
    data = resp.json()
    translated = {
        k: v["translatedText"]
        for k, v in zip(notes.keys(), data["data"]["translations"])
    }
    return translated
