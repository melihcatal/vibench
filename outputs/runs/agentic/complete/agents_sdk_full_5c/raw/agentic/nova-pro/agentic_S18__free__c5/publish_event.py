import os
from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(os.getenv('GCP_PROJECT'), os.getenv('GCP_TOPIC'))

def publish_event(data):
    data = data.encode('utf-8')
    future = publisher.publish(topic_path, data=data)
    print(future.result())

publish_event('{\"event\":\"test\"}')