from typing import Dict
import requests
from observability_client import get_metrics_config

TRANSLATION_HOST = "https://translation.googleapis.com"


def dashboard_note_translate(text: str, target_locale: str, source_locale: str = "en") -> Dict[str, str]:
    cfg = get_metrics_config()
    token = cfg.credentials_token
    if not token:
        raise ValueError("GOOGLE_OAUTH_ACCESS_TOKEN or GCP_ACCESS_TOKEN is required for Google Cloud Translation")
    url = f"{TRANSLATION_HOST}/language/translate/v2"
    params = {"q": text, "target": target_locale, "source": source_locale, "format": "text"}
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    resp = requests.post(url, headers=headers, params=params, timeout=cfg.timeout_seconds)
    resp.raise_for_status()
    data = resp.json()
    translated = data.get("data", {}).get("translations", [{}])[0].get("translatedText", "")
    return {"source": text, "target_locale": target_locale, "translated": translated}
