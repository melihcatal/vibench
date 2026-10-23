import json
from google.cloud import pubsub_v1
from messaging_client import PubSubClient
from messaging_models import PubSubMessage

# Configure client (uses GOOGLE_APPLICATION_CREDENTIALS env var)
client = PubSubClient(project_id='my-project', topic_id='my-topic')

# Example JSON event
event = {
    'id': 'e-12345',
    'type': 'order_created',
    'payload': {'order_id': 'ORD-001', 'amount': 250.0}
}

# Publish single message
message = PubSubMessage(event)
future = client.publisher.publish(client.topic_path, message.to_bytes())
print(f'Published message with ID: {future.result()}')
