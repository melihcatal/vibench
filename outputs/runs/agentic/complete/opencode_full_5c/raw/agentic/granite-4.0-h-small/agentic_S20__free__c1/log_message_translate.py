import json
from typing import List, Dict
from observability_client import get_log_service_url, get_auth_header


def translate_log_messages(
    events: List[Dict[str, Any]], target_locale: str = "es"
) -> List[Dict[str, Any]]:
    """Translate support-visible log messages for another locale.

    Provider: Translation API (example uses DeepL API placeholder).
    """
    url = get_log_service_url() + "/translate"
    headers = {
        **get_auth_header(),
        "Content-Type": "application/json",
    }
    payload = {"events": events, "target_locale": target_locale}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.json().get("translated_events", [])
