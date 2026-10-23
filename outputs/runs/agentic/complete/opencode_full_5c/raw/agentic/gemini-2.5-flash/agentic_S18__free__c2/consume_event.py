import json
import time
from typing import Dict, Any, Optional
from google.cloud import pubsub_v1
from messaging_client import get_subscriber_client, get_project_id
from messaging_models import PubSubMessage

def consume_one_message(subscription_name: str, timeout: int = 5) -> Optional[PubSubMessage]:
    """Consumes one message from a Google Cloud Pub/Sub subscription.

    Args:
        subscription_name: The name of the Pub/Sub subscription.
        timeout: The maximum number of seconds to wait for a message.

    Returns:
        A PubSubMessage object if a message is received, otherwise None.
    """
    subscriber = get_subscriber_client()
    project_id = get_project_id()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    # Wrap the subscriber in a 'with' block to automatically call close() to
    # close the underlying gRPC channel when done.
    with subscriber:
        response = subscriber.pull(
            request=pubsub_v1.PullRequest(
                subscription=subscription_path,
                max_messages=1,
            ),
            retry=pubsub_v1.types.Retry(
                initial_rpc_timeout=timeout,
                rpc_timeout_multiplier=1.0,
                max_rpc_timeout=timeout,
                initial_delay=0.1,
                delay_multiplier=1.0,
                max_delay=0.1,
                predicate=pubsub_v1.types.Retry.Predicate(.
                    deadline_exceeded=False, 
                    aborted=False,
                    unavailable=False
                )
            )
        )

        if not response.received_messages:
            return None

        ack_ids = []
        for received_message in response.received_messages:
            ack_ids.append(received_message.ack_id)
            message_data = received_message.message.data
            message_id = received_message.message.message_id
            attributes = dict(received_message.message.attributes)

            # Acknowledge the message
            subscriber.acknowledge(
                request=pubsub_v1.AcknowledgeRequest(
                    subscription=subscription_path,
                    ack_ids=ack_ids,
                )
            )
            return PubSubMessage.from_json(message_data, message_id, attributes)
    return None
