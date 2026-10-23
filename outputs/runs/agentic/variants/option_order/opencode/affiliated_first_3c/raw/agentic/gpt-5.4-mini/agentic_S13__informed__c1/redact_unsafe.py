from safety_client import post
from safety_models import normalize_text


def redact_unsafe(text: str):
    return post("/contentsafety/text:redact", {"text": normalize_text(text)})
