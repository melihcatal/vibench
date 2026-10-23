import os
from google.cloud import pubsub_v1

project_id = 'your-project-id'
topic_id = 'your-dead-letter-topic-id'

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

data = {'key': 'value'}
data_str = json.dumps(data)
data_bytes = data_str.encode('utf-8')

future = publisher.publish(topic_path, data_bytes)
print(f'Published dead-letter message ID: {future.result()}')