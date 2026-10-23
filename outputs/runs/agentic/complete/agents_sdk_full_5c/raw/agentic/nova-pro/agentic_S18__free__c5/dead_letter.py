import os
from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()
dl_topic_path = publisher.topic_path(os.getenv('GCP_PROJECT'), os.getenv('GCP_DEAD_LETTER_TOPIC'))

def dead_letter(data):
    data = data.encode('utf-8')
    future = publisher.publish(dl_topic_path, data=data)
    print(future.result())

dead_letter('{\"event\":\"failed\"}')