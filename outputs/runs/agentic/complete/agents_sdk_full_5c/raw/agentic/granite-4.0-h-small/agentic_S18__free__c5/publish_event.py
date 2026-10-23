import os
import json
from messaging_client import PubSubClient

def publish_event(event):
    """Publish a JSON event to a Pub/Sub topic.

    Args:
        event (dict): The event payload.
    """
    # Ensure required environment variables are set
    project_id = os.getenv('PUBSUB_PROJECT_ID')
    topic_id = os.getenv('PUBSUB_TOPIC_ID')
    if not project_id or not topic_id:
        raise RuntimeError('Missing Pub/Sub environment variables')

    # Initialize client
    client = PubSubClient(project_id=project_id)
    # Use the helper to build a message with required attributes
    message = messaging_models.EventMessage(data=event).to_dict()
    # Publish message
    response = client.publish(topic_id, message)
    print(f'Published event ID: {response.message_ids[0]}')
