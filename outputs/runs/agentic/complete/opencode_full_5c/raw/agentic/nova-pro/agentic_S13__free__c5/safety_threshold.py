from safety_client import SafetyClient


def apply_safety_threshold(text: str, threshold: float) -> bool:
    client = SafetyClient()
    response = client.moderate(text)
    return response["safety_score"] >= threshold
