import os
from google.cloud import pubsub_v1

# Configuration
project_id = 'your-project-id'
topic_id = 'your-topic-id'

# Authenticate
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# Batch publish messages
data_list = [{'key': 'value1'}, {'key': 'value2'}]
futures = []
for data in data_list:
    data_str = json.dumps(data)
    data_bytes = data_str.encode('utf-8')
    futures.append(publisher.publish(topic_path, data=data_bytes))
pubsub_v1.utilities.wait_for_futures(futures)