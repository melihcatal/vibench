import os
from google.cloud import pubsub_v1

project_id = 'your-project-id'
topic_id = 'your-dead-letter-topic-id'

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def send_to_dead_letter(message):
    future = publisher.publish(topic_path, message.encode('utf-8'))
    print(f'Sent to dead letter: {future.result()}')