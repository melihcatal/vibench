import json
from google.cloud import pubsub_v1
from messaging_client import PubSubClient
from messaging_models import PubSubMessage

client = PubSubClient(project_id='my-project', subscription_id='my-sub')

subscriber = pubsub_v1.SubscriberClient()
subscription_path = client.subscription_path

# Pull one message, ack after processing
response = subscriber.pull(request={'subscription': subscription_path, 'max_messages': 1})
if response.received_messages:
    msg = response.received_messages[0]
    data = json.loads(msg.message.data.decode('utf-8'))
    print('Consumed message:', data)
    subscriber.acknowledge(request={'subscription': subscription_path, 'ack_ids': [msg.ack_id]})
else:
    print('No messages available')
