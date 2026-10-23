import os
import json
import requests
from messaging_models import PubSubEvent, ConsumeResult


CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
API_VERSION = "2024-02-15-preview"


def check_message_safety(result: ConsumeResult) -> dict:
    event = result.to_event()
    if event is None:
        return {"error": "No valid event to check", "safe": False, "categories": {}}

    text_to_check = json.dumps(event.payload, ensure_ascii=False)
    if event.attributes:
        text_to_check += " " + json.dumps(event.attributes, ensure_ascii=False)

    endpoint = CONTENT_SAFETY_ENDPOINT.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze?api-version={API_VERSION}"
    headers = {
        "Ocp-Apim-Subscription-Key": CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }
    body = {
        "text": text_to_check,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=body, timeout=30)
    response.raise_for_status()
    analysis = response.json()

    categories = {}
    any_unsafe = False
    for category_result in analysis.get("categoriesAnalysis", []):
        cat = category_result.get("category", "unknown")
        severity = category_result.get("severity", 0)
        categories[cat] = severity
        if severity >= 2:
            any_unsafe = True

    return {
        "event_id": event.event_id,
        "message_id": result.message_id,
        "safe": not any_unsafe,
        "categories": categories,
        "blocklistsMatch": analysis.get("blocklistsMatch", []),
        "service": "Azure AI Content Safety",
    }


if __name__ == "__main__":
    evt = PubSubEvent(
        event_type="user.message",
        source="chat-service",
        payload={"text": "Hello, this is a normal message."},
    )
    cr = ConsumeResult(message_id="msg-safety-001", event=evt)
    safety_result = check_message_safety(cr)
    print(json.dumps(safety_result, indent=2))
