from safety_client import SafetyClient


def moderate_batch(texts: list) -> list:
    client = SafetyClient()
    responses = [client.moderate(text) for text in texts]
    return responses
