from safety_client import SafetyClient


def redact_unsafe(text: str) -> str:
    client = SafetyClient()
    response = client.moderate(text)
    if response["unsafe"]:
        return response["redacted_text"]
    return text
