import json
from google.cloud import pubsub_v1
from messaging_client import get_subscription_path

def consume_event():
    """
    consumes one message from a managed subscription or queue
    """
    subscription_path = get_subscription_path()
    subscriber = pubsub_v1.SubscriberClient()
    response = subscriber.pull(
        request={
            'subscription': subscription_path,
            'max_messages': 1
        }
    )
    messages = []
    for received_message in response.received_messages:
        data_str = received_message.message.data.decode('utf-8')
        message = {
            'data': json.loads(data_str),
            'attributes': dict(received_message.message.attributes),
            'message_id': received_message.message.message_id
        }
        messages.append(message)
        subscriber.acknowledge(
            request={
                'subscription': subscription_path,
                'ack_ids': [received_message.ack_id]
            }
        )
    return messages[0] if messages else None