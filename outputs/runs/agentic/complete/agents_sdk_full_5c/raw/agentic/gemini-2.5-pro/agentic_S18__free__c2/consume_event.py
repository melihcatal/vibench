from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from typing import Optional, Dict

from messaging_client import get_subscriber_client, get_subscription_path, MAIN_SUBSCRIPTION_ID

def consume_event() -> Optional[Dict]:
    """
    Consumes a single message from a Google Cloud Pub/Sub subscription.
    """
    subscriber = get_subscriber_client()
    subscription_path = get_subscription_path(MAIN_SUBSCRIPTION_ID)
    
    print(f"Listening for messages on {subscription_path}...")
    
    try:
        response = subscriber.pull(
            request={"subscription": subscription_path, "max_messages": 1}
        )
        if not response.received_messages:
            print("No messages received.")
            return None

        received_message = response.received_messages[0]
        message_data = received_message.message.data.decode("utf-8")
        
        print(f"Received message: {message_data}")
        
        subscriber.acknowledge(
            request={"subscription": subscription_path, "ack_ids": [received_message.ack_id]}
        )
        print(f"Acknowledged message: {received_message.ack_id}")
        
        return {
            "ack_id": received_message.ack_id,
            "data": message_data,
            "attributes": dict(received_message.message.attributes),
        }
        
    except TimeoutError:
        print("Pull request timed out.")
        return None
    except Exception as e:
        print(f"An error occurred while consuming message: {e}")
        return None
