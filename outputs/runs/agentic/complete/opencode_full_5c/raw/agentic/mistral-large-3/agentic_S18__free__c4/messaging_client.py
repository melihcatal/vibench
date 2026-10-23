import os
from google.cloud import pubsub_v1
from typing import Dict, Any, Optional
import json

# Provider-specific: Google Cloud Pub/Sub
# Environment variable: GOOGLE_APPLICATION_CREDENTIALS


def get_pubsub_client() -> Dict[str, Any]:
    """Initialize and return Pub/Sub clients for publishing and subscribing."""
    return {
        "publisher": pubsub_v1.PublisherClient(),
        "subscriber": pubsub_v1.SubscriberClient(),
    }


def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize payload for consistent processing."""
    return {
        "data": payload.get("data", {}),
        "attributes": payload.get("attributes", {}),
    }


def load_config() -> Dict[str, str]:
    """Load configuration from environment variables."""
    return {
        "project_id": os.getenv("GOOGLE_CLOUD_PROJECT_ID", ""),
        "topic_id": os.getenv("PUBSUB_TOPIC_ID", ""),
        "subscription_id": os.getenv("PUBSUB_SUBSCRIPTION_ID", ""),
        "dead_letter_topic_id": os.getenv("PUBSUB_DEAD_LETTER_TOPIC_ID", ""),
    }
