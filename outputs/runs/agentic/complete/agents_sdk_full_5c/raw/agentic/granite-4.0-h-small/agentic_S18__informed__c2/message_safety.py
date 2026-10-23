import os, requests
from messaging_models import PubSubMessage, ProcessingResult

def check_safety(message: PubSubMessage, api_key: str) -> bool:
    """Call Perspective API to detect toxic content in a message payload.

    Returns True if the message is safe, False otherwise.
    """
    payload = json.loads(message.data)
    text = payload.get("body", "")
    if not text:
        return True  # no text => nothing to moderate
    endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {"doNotStore": "true", "clientToken": str(uuid.uuid4())}
    headers = {"key": api_key, "Content-Type": "application/json"}
    data = {"comment": {"text": text}, "languages": ["en"], **params}
    response = requests.post(endpoint, json=data, headers=headers, timeout=10)
    if response.status_code != 200:
        raise RuntimeError(f"Perspective API error: {response.status_code} {response.text}")
    scores = response.json().get("attributeScores", {})
    toxicity = scores.get("TOXICITY", {}).get("summaryScore", {}).get("value", 0.0)
    # Threshold can be tuned; here we treat >=0.5 as unsafe
    return toxicity < 0.5

def safe_publish(original_msg: PubSubMessage, api_key: str, safe_topic: str) -> ProcessingResult:
    """Publish a message to a safe topic if it passes moderation; otherwise return failure.

    Returns a ProcessingResult indicating outcome.
    """
    if not check_safety(original_msg, api_key):
        return build_processing_result(original_msg.message_id, "failed", "unsafe_content")
    # Re‑publish to safe topic
    safe_msg = PubSubMessage(data=original_msg.data, attributes=original_msg.attributes)
    from messaging_client import PubSubClient
    client = PubSubClient()
    future = client.publish(safe_topic, safe_msg)
    future.result()  # wait for ack
    return build_processing_result(original_msg.message_id, "ok")

if __name__ == "__main__":
    # Demo (requires PERSPECTIVE_API_KEY env var set)
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("Missing PERSPECTIVE_API_KEY environment variable")
    # Minimal demo – would normally be called from a subscriber callback
    # safe_publish(original_msg, api_key, "projects/PROJECT/topics/safe-topic")
