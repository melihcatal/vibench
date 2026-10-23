from safety_client import analyze_text
from safety_models import SafetyResponse


def moderate_text(text: str) -> SafetyResponse:
    return analyze_text(text)
