import os
from google.cloud import pubsub_v1


def dead_letter(message, dead_letter_topic):
    project_id = "your-project-id"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, dead_letter_topic)

    message_data = message.encode("utf-8")
    publisher.publish(topic_path, message_data)

    print(f"Message sent to dead letter topic {dead_letter_topic}")
