from messaging_client import (
    get_subscriber_client,
    get_subscription_path,
    get_project_id,
)
from messaging_models import EventMessage
from google.cloud import datastore
import datetime
import os


def persist_message_record(
    subscription_id: str, kind: str = "MessageAudit", timeout: int = 5
):
    """Consumes a message and persists its record to Google Cloud Datastore.

    Args:
        subscription_id: The ID of the Pub/Sub subscription.
        kind: The Datastore kind to store the message under.
        timeout: The maximum number of seconds to wait for a message.

    Returns:
        The EventMessage object if a message is consumed and persisted, otherwise None.
    """
    project_id = get_project_id()
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    datastore_client = datastore.Client(project=project_id)

    subscriber = get_subscriber_client()
    subscription_path = get_subscription_path(project_id, subscription_id)

    response = subscriber.pull(
        request={
            "subscription": subscription_path,
            "max_messages": 1,
            "return_immediately": True,
        }
    )

    if response.received_messages:
        received_message = response.received_messages[0]
        ack_id = received_message.ack_id
        message = received_message.message

        event_message = EventMessage.from_pubsub_message(message)

        print(f"Received message ID: {event_message.id} for auditing.")

        try:
            key = datastore_client.key(kind, event_message.id)
            entity = datastore.Entity(key=key)

            entity["message_id"] = event_message.id
            entity["message_type"] = event_message.type
            entity["message_source"] = event_message.source
            entity["data"] = str(
                event_message.data
            )  # Store data as string or convert to a compatible format
            entity["attributes"] = str(
                event_message.attributes
            )  # Store attributes as string
            entity["timestamp"] = datetime.datetime.now(datetime.timezone.utc)

            datastore_client.put(entity)
            print(
                f"Message {event_message.id} persisted to Datastore under kind '{kind}'."
            )

            subscriber.acknowledge(
                request={"subscription": subscription_path, "ack_ids": [ack_id]}
            )
            return event_message

        except Exception as e:
            print(f"Error persisting message {event_message.id} to Datastore: {e}")
            subscriber.nack(
                request={"subscription": subscription_path, "ack_ids": [ack_id]}
            )
            return None
    else:
        print("No messages received for auditing.")
        return None


if __name__ == "__main__":
    # Example Usage (replace with your actual subscription_id)
    # Set GOOGLE_CLOUD_PROJECT environment variable before running
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # Make sure you have Cloud Datastore API enabled and permissions set up.
    example_subscription_id = "my-test-subscription"
    example_kind = "MyMessageAudit"

    # event = persist_message_record(example_subscription_id, example_kind)
    # if event:
    #     print(f"Audited Event: {event.id}")
