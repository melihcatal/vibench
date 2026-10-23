import re

from messaging_models import IntegrationResponse


def check_message_safety(payload_text: str):
    provider = "google_perspective_api"
    unsafe = bool(re.search(r"\b(hate|threat|violence|abuse)\b", payload_text or "", re.I))
    return IntegrationResponse(provider=provider, resource="message_safety", details={"unsafe": unsafe, "text": payload_text})
