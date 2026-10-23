import os
from typing import Dict, Any

# Example configuration loader using environment variables for provider selection
PROVIDER = os.getenv("PUBSUB_PROVIDER", "google")  # default to Google Cloud Pub/Sub


class PubSubClient:
    """Local helper for creating a provider‑specific Pub/Sub client."""

    def __init__(self):
        if PROVIDER == "google":
            from google.cloud import pubsub_v1

            self.publisher = pubsub_v1.PublisherClient()
            self.subscriber = pubsub_v1.SubscriberClient()
        elif PROVIDER == "aws":
            import boto3

            self.sns = boto3.client("sns")
            self.sqs = boto3.client("sqs")
        elif PROVIDER == "azure":
            from azure.servicebus import ServiceBusClient, ServiceBusMessage

            self.client = ServiceBusClient.from_connection_string(
                os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")
            )
        else:
            raise ValueError(f"Unsupported provider: {PROVIDER}")

    def publish(self, topic_name: str, message_body: str) -> None:
        if PROVIDER == "google":
            future = self.publisher.publish(
                f"projects/{os.getenv('GOOGLE_PROJECT_ID')}/topics/{topic_name}",
                data=message_body.encode(),
            )
            future.result()  # blocks until ack
        elif PROVIDER == "aws":
            self.sns.publish(
                TopicArn=os.getenv("AWS_SNS_TOPIC_ARN"), Message=message_body
            )
        elif PROVIDER == "azure":
            sender = self.client.get_queue_sender(
                queue_name=os.getenv("AZURE_QUEUE_NAME")
            )
            message = ServiceBusMessage(message_body)
            sender.send_messages(message)

    def consume(self, subscription_name: str) -> Any:
        if PROVIDER == "google":
            subscription_path = f"projects/{os.getenv('GOOGLE_PROJECT_ID')}/subscriptions/{subscription_name}"
            response = self.subscriber.pull(subscription_path, max_messages=1)
            if not response.received_messages:
                return None
            msg = response.received_messages[0]
            return msg
        else:
            raise NotImplementedError(
                f"Consuming not implemented for provider {PROVIDER}"
            )

    def publish_batch(self, topic_name: str, batch: list[str]) -> None:
        if PROVIDER == "google":
            self.publisher.publish_many(
                f"projects/{os.getenv('GOOGLE_PROJECT_ID')}/topics/{topic_name}",
                [data.encode() for data in batch],
            ).result()
        else:
            raise NotImplementedError(
                f"Batch publish not implemented for provider {PROVIDER}"
            )
