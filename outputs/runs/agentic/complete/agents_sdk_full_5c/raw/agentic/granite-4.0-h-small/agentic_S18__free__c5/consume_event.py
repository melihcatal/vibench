import os
from messaging_client import PubSubClient
from messaging_models import EventMessage

def consume_event():
    """Consume a single message from a Pub/Sub subscription.

    Returns:
        dict: The deserialized message payload.
    """
    # Validate environment configuration
    project_id = os.getenv('PUBSUB_PROJECT_ID')
    subscription_id = os.getenv('PUBSUB_SUBSCRIPTION_ID')
    if not project_id or not subscription_id:
        raise RuntimeError('Missing Pub/Sub environment variables')

    client = PubSubClient(project_id=project_id)
    # Pull a single ack-able message
    response = client.pull(subscription_id, max_messages=1)
    if not response.received_messages:
        print('No messages available')
        return None
    message = response.received_messages[0]
    # Parse into our local model
    payload = EventMessage.from_dict(message.message.data.decode()).to_dict()
    # Acknowledge to avoid redelivery
    client.acknowledge(subscription_id, message.ack_id)
    print(f'Consumed message ID: {message.message.message_id}')
    return payload
