from safety_client import SafetyClient
from safety_models import TextModerationRequest, ModerationResult


def moderate_text(text: str, language: str = "en") -> ModerationResult:
    client = SafetyClient()
    request: TextModerationRequest = {
        "text": text,
        "language": language
    }
    return client.analyze_text(request)