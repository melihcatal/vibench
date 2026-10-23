import os
from dataclasses import dataclass
from google.cloud import pubsub_v1


@dataclass(frozen=True)
class PubSubConfig:
    project_id: str
    topic_name: str
    subscription_name: str
    dead_letter_topic_name: str

    @property
    def topic_path(self):
        return f"projects/{self.project_id}/topics/{self.topic_name}"

    @property
    def subscription_path(self):
        return f"projects/{self.project_id}/subscriptions/{self.subscription_name}"

    @property
    def dead_letter_topic_path(self):
        return f"projects/{self.project_id}/topics/{self.dead_letter_topic_name}"


def get_pubsub_config():
    return PubSubConfig(
        project_id=os.environ["GOOGLE_CLOUD_PROJECT"],
        topic_name=os.environ.get("PUBSUB_TOPIC", "events"),
        subscription_name=os.environ.get("PUBSUB_SUBSCRIPTION", "events-sub"),
        dead_letter_topic_name=os.environ.get("PUBSUB_DEAD_LETTER_TOPIC", "events-dlq"),
    )


def get_publisher(config=None):
    config = config or get_pubsub_config()
    return pubsub_v1.PublisherClient()


def get_subscriber(config=None):
    config = config or get_pubsub_config()
    return pubsub_v1.SubscriberClient()
