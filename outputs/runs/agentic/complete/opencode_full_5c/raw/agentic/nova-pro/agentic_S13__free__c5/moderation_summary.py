from safety_client import SafetyClient


def summarize_moderation(texts: list) -> str:
    client = SafetyClient()
    responses = [client.moderate(text) for text in texts]
    summary = " ".join([str(response["unsafe"]) for response in responses])
    return summary
