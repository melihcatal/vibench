"""Local configuration and client helper utilities for Pub/Sub Messaging.

Provides centralized configuration loading, client initialization helpers,
and utility functions for the messaging integration layer.
"""

import os
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

# Google Cloud Pub/Sub configuration defaults
DEFAULT_GCP_PROJECT = "pubsub-project-001"
DEFAULT_PUBSUB_TOPIC = "events-topic"
DEFAULT_PUBSUB_SUBSCRIPTION = "events-subscription"
DEFAULT_DEAD_LETTER_TOPIC = "events-dlq"


@dataclass
class MessagingConfig:
    """Configuration for Google Cloud Pub/Sub messaging integration."""

    project_id: str = field(default_factory=lambda: os.environ.get("GOOGLE_CLOUD_PROJECT", DEFAULT_GCP_PROJECT))
    topic_name: str = field(default_factory=lambda: os.environ.get("PUBSUB_TOPIC", DEFAULT_PUBSUB_TOPIC))
    subscription_name: str = field(default_factory=lambda: os.environ.get("PUBSUB_SUBSCRIPTION", DEFAULT_PUBSUB_SUBSCRIPTION))
    dead_letter_topic_name: str = field(default_factory=lambda: os.environ.get("PUBSUB_DEAD_LETTER_TOPIC", DEFAULT_DEAD_LETTER_TOPIC))
    credentials_path: Optional[str] = field(default_factory=lambda: os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
    region: str = field(default_factory=lambda: os.environ.get("GCP_REGION", "us-central1"))

    @property
    def topic_path(self) -> str:
        """Return the full Pub/Sub topic path."""
        return f"projects/{self.project_id}/topics/{self.topic_name}"

    @property
    def subscription_path(self) -> str:
        """Return the full Pub/Sub subscription path."""
        return f"projects/{self.project_id}/subscriptions/{self.subscription_name}"

    @property
    def dead_letter_topic_path(self) -> str:
        """Return the full Pub/Sub dead-letter topic path."""
        return f"projects/{self.project_id}/topics/{self.dead_letter_topic_name}"

    def to_dict(self) -> Dict[str, str]:
        """Convert configuration to dictionary."""
        return {
            "project_id": self.project_id,
            "topic_name": self.topic_name,
            "subscription_name": self.subscription_name,
            "dead_letter_topic_name": self.dead_letter_topic_name,
            "region": self.region,
            "topic_path": self.topic_path,
            "subscription_path": self.subscription_path,
            "dead_letter_topic_path": self.dead_letter_topic_path,
        }


def load_config(env_prefix: str = "PUBSUB") -> MessagingConfig:
    """Load messaging configuration from environment variables.

    Args:
        env_prefix: Environment variable prefix to use.

    Returns:
        MessagingConfig instance populated from environment.
    """
    return MessagingConfig()


def get_publisher_options(
    batch_max_messages: int = 100,
    batch_max_bytes: int = 1024 * 1024,
    batch_max_latency: float = 0.05,
) -> Dict[str, Any]:
    """Return Google Cloud Pub/Sub publisher batch options.

    Args:
        batch_max_messages: Maximum messages per batch.
        batch_max_bytes: Maximum batch size in bytes.
        batch_max_latency: Maximum latency before sending batch.

    Returns:
        Dict with Pub/Sub PublisherClient batch settings.
    """
    from google.cloud.pubsub_v1.types import BatchSettings
    return BatchSettings(
        max_messages=batch_max_messages,
        max_bytes=batch_max_bytes,
        max_latency=batch_max_latency,
    )


def build_message_attributes(
    event_type: str,
    event_id: str,
    extra: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    """Build standardized Pub/Sub message attributes.

    Args:
        event_type: Event type identifier.
        event_id: Unique event identifier.
        extra: Additional attributes to include.

    Returns:
        Dict of message attributes.
    """
    attrs = {
        "event_type": event_type,
        "event_id": event_id,
        "content_type": "application/json",
    }
    if extra:
        attrs.update(extra)
    return attrs


def validate_pubsub_path(path: str, resource_type: str = "topic") -> bool:
    """Validate a Google Cloud Pub/Sub resource path format.

    Args:
        path: Path string to validate.
        resource_type: Expected resource type (topic or subscription).

    Returns:
        True if path matches expected format.
    """
    if resource_type == "topic":
        pattern = f"projects/{{project}}/topics/{{name}}"
        parts = path.split("/")
        return len(parts) == 4 and parts[0] == "projects" and parts[2] == "topics"
    elif resource_type == "subscription":
        parts = path.split("/")
        return len(parts) == 4 and parts[0] == "projects" and parts[2] == "subscriptions"
    return False
