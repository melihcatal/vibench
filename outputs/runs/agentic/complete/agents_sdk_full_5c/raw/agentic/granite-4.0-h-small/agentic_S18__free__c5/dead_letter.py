import os
from messaging_client import PubSubClient
from messaging_models import EventMessage

def dead_letter(message):
    """Send a message to a dead-letter topic after processing failure.

    Args:
        message (ReceivedMessage): The message object from the consumer.
    """
    project_id = os.getenv('PUBSUB_PROJECT_ID')
    dl_topic_id = os.getenv('PUBSUB_DEADLETTER_TOPIC_ID')
    if not dl_topic_id:
        raise RuntimeError('Missing dead-letter topic environment variable')

    client = PubSubClient(project_id=project_id)
    # Convert to our JSON payload for consistency
    payload = EventMessage.from_dict(message.message.data.decode()).to_dict()
    # Publish to dead-letter topic
    client.publish(dl_topic_id, payload)
    print(f'Dead-lettered message ID: {message.message.message_id}')
