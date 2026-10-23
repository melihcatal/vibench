import os
import requests
from typing import Dict, Any
from messaging_models import DeadLetterPayload, PublishRequest
from messaging_client import get_kafka_client

# Example: Perspective API integration (could be swapped for another service)
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")

HEADERS = {
    "x-api-key": PERSPECTIVE_API_KEY,
    "Content-Type": "application/json",
}


def check_unsafe_content(text: str) -> bool:
    """
    Return True if the text contains unsafe content (toxicity score > threshold).
    """
    threshold = 0.8
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    resp = requests.post(PERSPECTIVE_API_URL, headers=HEADERS, json=payload)
    if resp.status_code != 200:
        # propagate error to caller or DLQ
        raise RuntimeError(f"Perspective API error {resp.status_code}")
    score = resp.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return score > threshold


def process_publish_request(req: PublishRequest, dlq_topic: str) -> bool:
    """
    Validate payload text; DLQ message if unsafe.
    """
    if not check_unsafe_content(req.payload.get("text", "")):
        return True  # safe - allow publish
    # unsafe => send to dead letter
    dl_payload = DeadLetterPayload(
        original_topic=req.topic,
        key=req.key,
        raw_message=json.dumps(req.payload),
        error="Unsafe content detected",
    )
    send_to_dead_letter(
        topic=req.topic,
        msg_key=req.key,
        raw_msg=json.dumps(req.payload),
        error="Unsafe content",
    )
    return False


# helper stub for DLQ (refer to dead_letter.py for full implementation)
def send_to_dead_letter(original_topic: str, msg_key: str, raw_msg: str, error: str):
    # placeholder - actual implementation in dead_letter.py
    print(f"[DLQ] {original_topic} key={msg_key} error={error}")


if __name__ == "__main__":
    # quick test (remove in prod)
    test_req = PublishRequest(
        topic="demo", payload={"text": "This is a safe test.", "id": "1"}
    )
    print("Safe?", check_unsafe_content(test_req.payload["text"]))
