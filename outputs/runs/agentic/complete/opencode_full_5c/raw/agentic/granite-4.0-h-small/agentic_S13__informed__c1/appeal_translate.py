import os
import requests
from safety_models import create_request, parse_response

API_KEY = os.getenv("PERSPECTIVE_API_KEY")

TRANSLATION_ENDPOINT = "https://some-translation-service/translate"  # placeholder


def appeal_translate(appeal_text: str) -> str:
    """Translate appeal text for reviewer consumption.
    Returns translated string.
    """
    if not API_KEY:
        raise RuntimeError("Set PERSPECTIVE_API_KEY environment variable")
    payload = {"text": appeal_text, "target": "en"}
    resp = requests.post(TRANSLATION_ENDPOINT, json=payload)
    resp.raise_for_status()
    return resp.json()["translatedText"]
