import os
from google.cloud import pubsub_v1


def publish_event(topic_name, message):
    project_id = "your-project-id"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    message_data = message.encode("utf-8")
    publisher.publish(topic_path, message_data)

    print(f"Message published to topic {topic_name}")
