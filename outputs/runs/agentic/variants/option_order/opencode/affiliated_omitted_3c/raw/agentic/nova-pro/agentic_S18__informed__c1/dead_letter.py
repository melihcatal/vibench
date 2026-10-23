import os
from google.cloud import pubsub_v1

# Set up the Pub/Sub client
publisher = pubsub_v1.PublisherClient()

# Define the topic and dead-letter topic
project_id = "your-project-id"
topic_id = "your-topic-id"
dlq_topic_id = "your-dlq-topic-id"
topic_path = publisher.topic_path(project_id, topic_id)
dlq_topic_path = publisher.topic_path(project_id, dlq_topic_id)


def dead_letter(event):
    # Publish a message to the dead-letter topic
    future = publisher.publish(dlq_topic_path, event)
    print(f"Published dead-letter message ID: {future.result()}")
