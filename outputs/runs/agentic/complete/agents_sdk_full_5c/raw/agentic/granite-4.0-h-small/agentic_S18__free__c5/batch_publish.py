import os
import json
from messaging_client import PubSubClient
from messaging_models import EventMessage

def batch_publish(events):
    """Publish multiple JSON events to a Pub/Sub topic.

    Args:
        events (List[dict]): List of event payloads.
    """
    project_id = os.getenv('PUBSUB_PROJECT_ID')
    topic_id = os.getenv('PUBSUB_TOPIC_ID')
    if not project_id or not topic_id:
        raise RuntimeError('Missing Pub/Sub environment variables')

    client = PubSubClient(project_id=project_id)
    # Convert each event using our model to ensure consistent attributes
    messages = [EventMessage(data=e).to_dict() for e in events]
    # Pub/Sub API supports a list of messages for batch publish
    response = client.publish(topic_id, messages)
    print(f'Batch published {len(response.message_ids)} messages')
