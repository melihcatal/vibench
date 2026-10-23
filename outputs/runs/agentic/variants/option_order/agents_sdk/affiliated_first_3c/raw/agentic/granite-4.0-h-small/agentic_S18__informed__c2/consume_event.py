import os
from messaging_client import PubSubClient

SUBSCRIPTION = os.getenv('PUBSUB_SUBSCRIPTION', 'my-sub')

def consume_event():
    """Consume a single message from the Pub/Sub subscription.
    Uses Google Cloud Pub/Sub SDK.
    """
    client = PubSubClient()
    message = client.pull(subscription=SUBSCRIPTION, max_messages=1)
    if not message:
        print('No message available.')
        return None
    payload = json.loads(message['data'].decode('utf-8'))
    print(f'Consumed message id={message["message_id"]}: {payload}')
    # Acknowledge after processing
    client.acknowledge(subscription=SUBSCRIPTION, message_ids=[message['message_id']])
    return payload
