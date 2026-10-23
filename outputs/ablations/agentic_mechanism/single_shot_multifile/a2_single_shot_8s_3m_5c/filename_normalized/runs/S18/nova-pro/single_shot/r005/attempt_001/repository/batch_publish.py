import os
from google.cloud import pubsub_v1

project_id = 'your-project-id'
topic_id = 'your-topic-id'

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

data_batch = [{'key': 'value1'}, {'key': 'value2'}]
futures = []
for data in data_batch:
    data_str = json.dumps(data)
    data_bytes = data_str.encode('utf-8')
    futures.append(publisher.publish(topic_path, data_bytes))

for future in futures:
    print(f'Published batch message ID: {future.result()}')