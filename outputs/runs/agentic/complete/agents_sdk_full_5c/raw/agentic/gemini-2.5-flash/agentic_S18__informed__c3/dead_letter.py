from messaging_client import get_subscriber_client, get_project_id
from messaging_models import PubSubMessage

def dead_letter_message(subscription_id: str, ack_id: str, success: bool):
    subscriber = get_subscriber_client()
    project_id = get_project_id()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    if success:
        print(f"Acknowledging message with ack_id: {ack_id}")
        subscriber.acknowledge(request={
            "subscription": subscription_path,
            "ack_ids": [ack_id]
        })
    else:
        print(f"Negatively acknowledging message with ack_id: {ack_id} for dead-lettering.")
        # If a dead-letter topic is configured for this subscription, 
        # the message will be moved there after max delivery attempts.
        subscriber.modify_ack_deadline(request={
            "subscription": subscription_path,
            "ack_ids": [ack_id],
            "ack_deadline_seconds": 0 # Immediately nack
        })
