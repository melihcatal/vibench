# messaging_client.py
# LOCAL HELPER: thin wrapper around Google Cloud Pub/Sub for common configuration and publishing helpers

import os
import json
from google.cloud import pubsub_v1
from google.auth import credentials

# Detect project ID from environment or default
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project")

# Google Cloud Pub/Sub Producer helper
class PubSubProducer:
    def __init__(self, project_id: str = None, credentials: credentials.Credentials = None):
        self.publisher = pubsub_v1.PublisherClient(credentials=credentials)
        self.project_id = project_id or PROJECT_ID

    def publish(self, topic_id: str, payload: dict):
        """Publish a JSON payload to a Pub/Sub topic.

        Args:
            topic_id: Topic name (e.g., "orders").
            payload: JSON‑serializable dictionary.
        Returns:
            The message ID string returned by the service.
        """
        data = json.dumps(payload).encode('utf-8')
        topic_path = self.publisher.topic_path(self.project_id, topic_id)
        return self.publisher.publish(topic_path, data=data).result()

# Google Cloud Pub/Sub Consumer helper
class PubSubConsumer:
    def __init__(self, project_id: str = None, subscription_id: str = None, credentials: credentials.Credentials = None):
        self.subscriber = pubsub_v1.SubscriberClient(credentials=credentials)
        self.project_id = project_id or PROJECT_ID
        self.subscription_id = subscription_id
        self.subscription_path = self.subscriber.subscription_path(self.project_id, self.subscription_id)

    def pull_one(self) -> dict | None:
        """Pull a single message, decode JSON, and acknowledge.

        Returns:
            Decoded payload dict or None if no message is available.
        """
        response = self.subscriber.pull(request={
            "subscription": self.subscription_path,
            "max_messages": 1,
            "return_immediately": False,
        })
        if not response.received_messages:
            return None
        received = response.received_messages[0]
        payload = json.loads(received.message.data.decode('utf-8'))
        self.subscriber.acknowledge(request={
            "subscription": self.subscription_path,
            "ack_ids": [received.ack_id],
        })
        return payload

# Helper to create a dead‑letter publisher (uses same project)
class DeadLetterPublisher:
    def __init__(self, project_id: str = None, credentials: credentials.Credentials = None):
        self.publisher = pubsub_v1.PublisherClient(credentials=credentials)
        self.project_id = project_id or PROJECT_ID

    def send(self, original_topic: str, dl_topic: str, payload: dict):
        """Encode a failure payload and forward it to a dead‑letter topic.

        Args:
            original_topic: Topic where the error was observed.
            dl_topic: Dead‑letter topic name.
            payload: The original payload that caused the failure.
        """
        data = json.dumps(
            {
                "original_topic": original_topic,
                "failed_payload": payload,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        ).encode('utf-8')
        dl_path = self.publisher.topic_path(self.project_id, dl_topic)
        self.publisher.publish(dl_path, data=data).result()

# Example configuration (normally loaded from env vars or a config file)
positional_args = {
    "producer": PubSubProducer(),
    "consumer": None,
    "dead_letter": DeadLetterPublisher(),
}

# Typical usage skeleton:
# producer = positional_args[\"producer\"]
# producer.publish(\"my-topic\", {\"event\":\"test\"})
# consumer = PubSubConsumer(subscription_id=\"my-sub\")
# payload = consumer.pull_one()
# if payload and \"error\" in payload:\n#     dl = positional_args[\"dead_letter\"]
#     dl.send(\"my-topic\", \"dl-my-topic\", payload)
