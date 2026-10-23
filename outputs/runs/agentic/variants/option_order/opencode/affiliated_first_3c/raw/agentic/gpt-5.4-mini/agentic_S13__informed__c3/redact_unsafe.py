from safety_client import SafetyClient
from safety_models import normalize_text


client = SafetyClient()


def redact_unsafe(text: str):
    payload = client.post("/text:redact", {"text": normalize_text(text)})
    return payload
