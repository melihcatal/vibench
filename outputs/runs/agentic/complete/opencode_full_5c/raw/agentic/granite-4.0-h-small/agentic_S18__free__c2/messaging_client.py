import os
import json

# Placeholder client handling multiple concrete providers.
# Real implementation should instantiate the appropriate provider client.


class MessagingClient:
    """Simple unified client for different messaging providers.

    This stub holds configuration details for the selected concrete provider
    and exposes generic publish / receive / dead_letter methods.
    """

    def __init__(
        self,
        project_id=None,  # Google Cloud
        topic_name=None,  # Google Cloud
        queue_url=None,  # AWS SQS
        dead_letter_queue=None,  # Azure
        exchange=None,  # RabbitMQ
        routing_key=None,
    ):  # RabbitMQ
        self.provider = None
        if project_id and topic_name:
            self.provider = "google_pubsub"
            self.project_id = project_id
            self.topic_name = topic_name
        elif queue_url:
            self.provider = "aws_sqs"
            self.queue_url = queue_url
        elif dead_letter_queue:
            self.provider = "azure_servicebus"
            self.dead_letter_queue = dead_letter_queue
        elif exchange and routing_key:
            self.provider = "rabbitmq"
            self.exchange = exchange
            self.routing_key = routing_key
        else:
            raise ValueError("Insufficient configuration for a provider")

    def publish(self, message):
        """Publish a single message to the configured provider."""
        if self.provider == "google_pubsub":
            print(
                f"[Pub/Sub] Publishing to {self.topic_name} (project {self.project_id})"
            )
        elif self.provider == "aws_sqs":
            print(f"[SQS] Sending to {self.queue_url}")
        elif self.provider == "azure_servicebus":
            print(f"[Service Bus] Dead‑letter queue: {self.dead_letter_queue}")
        elif self.provider == "rabbitmq":
            print(
                f"[RabbitMQ] Publishing to exchange {self.exchange} (key {self.routing_key})"
            )
        else:
            print("[UNKNOWN] MessagingClient stub: no publish implementation")

    def receive_messages(self, max_count=1):
        """Stub for receiving messages."""
        if self.provider == "aws_sqs":
            print(f"[SQS] Receiving up to {max_count} messages from {self.queue_url}")
            return []  # empty list as placeholder
        return []

    def send_dead_letter(self, message):
        if self.provider == "azure_servicebus":
            print(
                f"[Azure] Moving {message.get('id')} to dead‑letter queue {self.dead_letter_queue}"
            )
        else:
            print("[UNKNOWN] No dead‑letter implementation")
