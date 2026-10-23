from safety_client import SafetyClient
from safety_models import ModerationRequest, normalize_text, parse_decision


client = SafetyClient()


def moderate_text(text: str):
    request = ModerationRequest(text=normalize_text(text))
    payload = client.post("/text:analyze", {"text": request.text, "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]})
    return parse_decision(payload)
