from messaging_client import get_publisher_client, get_project_id
from messaging_models import PubSubMessage

def publish_event(topic_id: str, message: PubSubMessage):
    publisher = get_publisher_client()
    project_id = get_project_id()
    topic_path = publisher.topic_path(project_id, topic_id)

    future = publisher.publish(topic_path, message.to_json_bytes(), **message.attributes)
    print(f"Published message ID: {future.result()}")
    return future.result()
