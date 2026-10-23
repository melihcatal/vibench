from safety_client import post
from safety_models import SafetyTextRequest, normalize_text


def moderate_text(text: str, language: str = None):
    req = SafetyTextRequest(text=normalize_text(text), language=language)
    payload = {"text": req.text, "language": req.language}
    return post("/contentsafety/text:analyze", payload)
