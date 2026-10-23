import os
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

from messaging_client import get_subscriber, SUBSCRIPTION_PATH

def consume_event():
    """
    Consumes a single message from the Google Cloud Pub/Sub subscription.
    """
    subscriber = get_subscriber()
    
    ack_ids = []
    message_data = None

    try:
        # The subscriber pulls a specific number of messages.
        response = subscriber.pull(
            request={"subscription": SUBSCRIPTION_PATH, "max_messages": 1},
            retry=None,
        )

        if not response.received_messages:
            print("No messages received.")
            return None

        for received_message in response.received_messages:
            print(f"Received: {received_message.message.data.decode('utf-8')}")
            message_data = received_message.message.data
            ack_ids.append(received_message.ack_id)

        # Acknowledges the received messages so they will not be sent again.
        if ack_ids:
            subscriber.acknowledge(
                request={"subscription": SUBSCRIPTION_PATH, "ack_ids": ack_ids}
            )
            print(f"Acknowledged {len(ack_ids)} message(s).")
        
        return message_data

    except TimeoutError:
        print("Pull request timed out.")
        return None
    except Exception as e:
        print(f"An error occurred during consumption: {e}")
        return None
