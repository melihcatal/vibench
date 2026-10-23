import json
from typing import List, Dict
from messaging_client import get_publisher_client, get_topic_path
from google.cloud.pubsub_v1.publisher.futures import Future


def batch_publish(topic_id: str, messages: List[Dict]):
    publisher = get_publisher_client()
    topic_path = get_topic_path(topic_id)

    publish_futures: List[Future] = []

    for message_data in messages:
        data = json.dumps(message_data).encode("utf-8")
        future = publisher.publish(
            topic_path,
            data,
            message_id=message_data.get("messageId", ""),
            **message_data.get("attributes", {}),
        )
        publish_futures.append(future)

    results = [future.result() for future in publish_futures]
    return results
