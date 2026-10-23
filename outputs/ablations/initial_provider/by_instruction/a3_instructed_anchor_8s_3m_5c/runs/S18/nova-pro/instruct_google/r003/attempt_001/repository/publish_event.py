from google.cloud import pubsub_v1

project_id = "your-project-id"
topic_id = "your-topic-id"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def publish_event(data):
    data = bytes(data, encoding='utf8')
    future = publisher.publish(topic_path, data)
    print(f'Published message ID: {future.result()}')