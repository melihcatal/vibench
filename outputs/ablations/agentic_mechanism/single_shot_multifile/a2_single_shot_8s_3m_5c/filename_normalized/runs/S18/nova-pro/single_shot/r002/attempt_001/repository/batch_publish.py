import os
from google.cloud import pubsub_v1

project_id = 'your-project-id'
topic_id = 'your-topic-id'

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def batch_publish(events):
    futures = publisher.publish_batch(topic_path, events)
    for future in futures:
        print(f'Published message ID: {future.result()}')