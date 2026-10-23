import os
from messaging_client import get_pubsub_subscriber_client
from messaging_models import EventMessage
import json


def consume_event(subscription_id: str, timeout: int = 5) -> EventMessage | None:
    subscriber = get_pubsub_subscriber_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1},
        retry=None,
        timeout=timeout,
    )

    if response.received_messages:
        for received_message in response.received_messages:
            message_data = received_message.message.data.decode("utf-8")
            attributes = dict(received_message.message.attributes)
            message_id = received_message.message.message_id

            # Acknowledge the message
            subscriber.acknowledge(
                request={
                    "subscription": subscription_path,
                    "ack_ids": [received_message.ack_id],
                }
            )

            # Assuming the message_data is a JSON string of EventMessage
            event_dict = json.loads(message_data)
            return EventMessage(
                id=event_dict.get("id", message_id),
                data=event_dict.get("data", {}),
                attributes=attributes,
            )
    return None


if __name__ == "__main__":
    pass
