import os
from google.cloud import pubsub_v1

# Configuration
project_id = 'your-project-id'
topic_id = 'your-dead-letter-topic-id'

# Authenticate
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# Publish a dead letter message
data = {'key': 'value'}
data_str = json.dumps(data)
data_bytes = data_str.encode('utf-8')
publisher.publish(topic_path, data=data_bytes)