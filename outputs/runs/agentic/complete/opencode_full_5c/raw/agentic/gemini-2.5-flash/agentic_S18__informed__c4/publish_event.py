import os
from messaging_client import get_pubsub_publisher_client
from messaging_models import EventMessage


def publish_event(topic_id: str, message: EventMessage) -> str:
    publisher = get_pubsub_publisher_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    topic_path = publisher.topic_path(project_id, topic_id)
    future = publisher.publish(
        topic_path, message.to_json(), **(message.attributes or {})
    )
    message_id = future.result()
    return message_id


if __name__ == "__main__":
    pass
