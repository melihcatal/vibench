import json
from google.cloud import pubsub_v1
from messaging_client import PubSubClient
from messaging_models import PubSubMessage

client = PubSubClient(project_id='my-project', topic_id='my-dead-letter-topic')

# Function to publish a failed message to a dead-letter topic
async def dead_letter_message(original_msg, reason):
    dl_client = PubSubClient(project_id='my-project', topic_id='my-dead-letter-topic')
    dl_msg = PubSubMessage(
        id=original_msg.id,
        type='dead_letter',
        payload={'original_id': original_msg.id, 'reason': reason}
    )
    future = dl_client.publisher.publish(dl_client.topic_path, dl_msg.to_bytes())
    await future
    print(f'Dead-lettered message {original_msg.id} due to {reason}')
