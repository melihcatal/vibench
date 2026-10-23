import safety_client


def redact_unsafe(text):
    client = safety_client.get_client()
    response = client.moderate_text(text)
    if response.get("safety_score") < 0.5:
        return response.get("redacted_text")
    return text
