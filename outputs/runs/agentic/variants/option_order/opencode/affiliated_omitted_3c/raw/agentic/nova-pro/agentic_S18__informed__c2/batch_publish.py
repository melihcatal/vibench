import os
from google.cloud import pubsub_v1


def batch_publish(topic_name, messages):
    project_id = "your-project-id"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    future_results = []
    for message in messages:
        message_data = message.encode("utf-8")
        future_results.append(publisher.publish(topic_path, message_data))

    for future in future_results:
        future.result()

    print(f"Batch messages published to topic {topic_name}")
