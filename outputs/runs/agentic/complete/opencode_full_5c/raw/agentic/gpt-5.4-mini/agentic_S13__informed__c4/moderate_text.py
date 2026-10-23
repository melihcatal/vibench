from safety_client import TisaneSafetyClient
from safety_models import SafetyRequest


def moderate_text(text: str, language: str = "en"):
    return TisaneSafetyClient().moderate_request(
        SafetyRequest(text=text, language=language)
    )
