from safety_client import SafetyClient
from safety_models import normalize_messages


client = SafetyClient()


def moderate_batch(messages):
    normalized = normalize_messages(messages)
    payload = client.post("/text:analyzeBatch", {"messages": normalized})
    return payload.get("items", payload)
