from safety_client import SafetyClient


def redact_unsafe(text: str, threshold: float = 0.5):
    return SafetyClient().redact_unsafe(text, threshold=threshold)
