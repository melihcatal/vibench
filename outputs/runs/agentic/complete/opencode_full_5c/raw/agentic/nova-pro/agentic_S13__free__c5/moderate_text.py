from safety_client import SafetyClient


def score_text(text: str) -> dict:
    client = SafetyClient()
    response = client.moderate(text)
    return response
