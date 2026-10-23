import os
import json
from google.cloud import pubsub_v1
from messaging_client import get_subscriber, SUBSCRIPTION_PATH

def consume_one_message():
    """Consumes a single message from a Pub/Sub subscription."""
    subscriber = get_subscriber()

    with subscriber:
        response = subscriber.pull(
            request={"subscription": SUBSCRIPTION_PATH, "max_messages": 1},
            retry=None,
        )

        if not response.received_messages:
            print("No messages received.")
            return None

        ack_ids = []
        message_data = None
        for received_message in response.received_messages:
            print(f"Received: {received_message.message.data.decode('utf-8')}")
            message_data = json.loads(received_message.message.data.decode('utf-8'))
            ack_ids.append(received_message.ack_id)

        # Acknowledge the message so it's not delivered again.
        if ack_ids:
            subscriber.acknowledge(
                request={"subscription": SUBSCRIPTION_PATH, "ack_ids": ack_ids}
            )
            print(f"Acknowledged {len(ack_ids)} message(s).")
        
        return message_data

