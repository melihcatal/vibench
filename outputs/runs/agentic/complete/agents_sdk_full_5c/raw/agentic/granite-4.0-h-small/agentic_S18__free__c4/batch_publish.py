import json
from google.cloud import pubsub_v1
from messaging_client import PubSubClient
from messaging_models import PubSubMessage

client = PubSubClient(project_id='my-project', topic_id='my-topic')

# Publish a batch of messages using Pub/Sub v1 batching
messages = [
    {'id': 'b-1', 'type': 'order_created', 'payload': {'order_id': 'ORD-010', 'amount': 100.0}},
    {'id': 'b-2', 'type': 'order_updated', 'payload': {'order_id': 'ORD-010', 'status': 'shipped'}},
    {'id': 'b-3', 'type': 'order_canceled', 'payload': {'order_id': 'ORD-010', 'reason': 'customer_cancelled'}},
]

pub_messages = [PubSubMessage(msg).to_bytes() for msg in messages]
future = client.publisher.publish(client.topic_path, *pub_messages)
result = future.result()
print(f'Batch published messages, message IDs: {result}')
