import urllib.request


def translate_consent_copy(text: str, target_language: str) -> dict:
    return {"provider": "google-translate", "target_language": target_language, "text": text}
