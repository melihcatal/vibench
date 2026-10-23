import os
from google.cloud import pubsub_v1

# Set up the Pub/Sub client
publisher = pubsub_v1.PublisherClient()

# Define the topic
project_id = "your-project-id"
topic_id = "your-topic-id"
topic_path = publisher.topic_path(project_id, topic_id)


def batch_publish(events):
    # Publish a batch of messages to the topic
    futures = publisher.publish_batch(topic_path, events)
    for future in futures:
        print(f"Published batch message ID: {future.result()}")
