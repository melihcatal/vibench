import json
from messaging_client import get_publisher_client, get_project_id, get_topic_path
from messaging_models import PubSubMessage


def batch_publish(topic_id: str, messages: list[dict]):
    publisher = get_publisher_client()
    project_id = get_project_id()
    topic_path = get_topic_path(project_id, topic_id)

    futures = []
    for msg_data in messages:
        message = PubSubMessage(
            msg_data["data"], attributes=msg_data.get("attributes", {})
        )
        data = message.to_json().encode("utf-8")
        future = publisher.publish(topic_path, data, **message.attributes)
        futures.append(future)

    message_ids = []
    for future in futures:
        message_ids.append(future.result())
    print(f"Published batch of messages with IDs: {message_ids}")
    return message_ids
