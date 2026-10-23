import os
from google.cloud import pubsub_v1

project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
dlq_topic_id = "your-dlq-topic-id"
dlq_publisher = pubsub_v1.PublisherClient()
dlq_topic_path = dlq_publisher.topic_path(project_id, dlq_topic_id)


def dead_letter(data):
    data = data.encode("utf-8")
    future = dlq_publisher.publish(dlq_topic_path, data)
    print(f"Published dead letter message ID: {future.result()}")
