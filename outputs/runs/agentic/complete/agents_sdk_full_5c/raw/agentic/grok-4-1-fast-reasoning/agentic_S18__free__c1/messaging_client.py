import os

GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID")
TOPIC_ID: str = os.getenv("TOPIC_ID")
SUBSCRIPTION_ID: str = os.getenv("SUBSCRIPTION_ID")
DLQ_TOPIC_ID: str = os.getenv("DLQ_TOPIC_ID")

def topic_path(topic_id: str) -> str:
    return f"projects/{GCP_PROJECT_ID}/topics/{topic_id}"

def subscription_path(subscription_id: str) -> str:
    return f"projects/{GCP_PROJECT_ID}/subscriptions/{subscription_id}"
