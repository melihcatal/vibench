import os
import time
from concurrent.futures import TimeoutError
from messaging_client import PubSubClient
from messaging_models import EventPayload

# Google Cloud Pub/Sub provider-identifying signal: google.cloud.pubsub_v1


def consume_event(subscription_id: str, timeout: int = 5) -> Optional[EventPayload]:
    """Consumes one message from a Google Cloud Pub/Sub subscription and acknowledges it."""
    client = PubSubClient()
    subscription_path = client.get_subscription_path(subscription_id)

    # Wrap the subscriber in a 'with' block to automatically call close() to release resources.
    with client.subscriber as subscriber:
        pull_futures = subscriber.pull(
            request=pubsub_v1.types.PullRequest(
                subscription=subscription_path,
                max_messages=1,
            ),
            retry=pubsub_v1.types.Retry(deadline=timeout),
        )

        response = pull_futures.result(timeout=timeout)

        if not response.received_messages:
            return None

        received_message = response.received_messages[0]
        message = received_message.message

        # Acknowledge the message
        ack_ids = [received_message.ack_id]
        subscriber.acknowledge(
            request=pubsub_v1.types.AcknowledgeRequest(
                subscription=subscription_path, ack_ids=ack_ids
            )
        )

        # Decode and parse the message
        event_payload = EventPayload.from_json_string(message.data.decode("utf-8"))

        return event_payload
