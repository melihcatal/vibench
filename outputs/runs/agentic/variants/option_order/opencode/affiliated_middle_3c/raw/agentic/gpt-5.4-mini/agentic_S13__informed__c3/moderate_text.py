from safety_client import SafetyClient
from safety_models import TextModerationRequest


def moderate_text(text: str, language: str | None = None):
    return SafetyClient().moderate_text(TextModerationRequest(text=text, language=language))
