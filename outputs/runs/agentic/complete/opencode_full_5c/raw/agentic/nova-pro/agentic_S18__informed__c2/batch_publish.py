import os
from google.cloud import pubsub_v1

project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
topic_id = 'your-topic-id'

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def batch_publish(messages):
    futures = []
    for data in messages:
        data = data.encode('utf-8')
        future = publisher.publish(topic_path, data)
        futures.append(future)
    print(f'Published batch message IDs: {[future.result() for future in futures]]')