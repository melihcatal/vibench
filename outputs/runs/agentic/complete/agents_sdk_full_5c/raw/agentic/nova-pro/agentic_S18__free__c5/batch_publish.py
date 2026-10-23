import os
from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(os.getenv('GCP_PROJECT'), os.getenv('GCP_TOPIC'))

def batch_publish(messages):
    futures = []
    for data in messages:
        data = data.encode('utf-8')
        futures.append(publisher.publish(topic_path, data=data))
    for future in futures:
        print(future.result())

batch_publish([{\"event\":\"batch1\"}, {\"event\":\"batch2\"}])