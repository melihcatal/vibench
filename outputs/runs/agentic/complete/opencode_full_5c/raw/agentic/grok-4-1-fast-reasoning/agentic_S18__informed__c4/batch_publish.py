from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.types import PubsubMessage
from typing import List, Dict, Any
from messaging_client import PubSubClient
from messaging_models import encode_message_data


def batch_publish(events: List[Dict[str, Any]]) -> List[str]:
    client = PubSubClient()
    pubsub_messages: List[PubsubMessage] = [
        PubsubMessage(data=encode_message_data(event)) for event in events
    ]
    response = client.publisher.publish_messages(
        topic=client.topic_path, messages=pubsub_messages
    )
    message_ids = [result.message_id for result in response.results]
    return message_ids
