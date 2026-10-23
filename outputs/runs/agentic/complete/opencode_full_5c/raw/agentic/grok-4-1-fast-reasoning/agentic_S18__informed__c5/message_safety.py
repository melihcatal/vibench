import requests
import os
from datetime import datetime
from uuid import uuid4
from messaging_models import MessageEvent, MessagePayload


def analyze_safety(event: MessageEvent) -> float:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": event.payload.message},
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(url, json=payload)
    data = response.json()
    score = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return float(score)


if __name__ == "__main__":
    event = MessageEvent(
        event_id=str(uuid4()),
        timestamp=datetime.utcnow().isoformat(),
        payload=MessagePayload(
            customer_name="Test User",
            order_id="SAFE-789",
            message="This is a normal customer complaint about delivery.",
        ),
    )
    score = analyze_safety(event)
    print(f"Toxicity score: {score}")
