from google.cloud import pubsub_v1

def publish_event(project_id, topic_id, data):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    data = data.encode('utf-8')
    future = publisher.publish(topic_path, data)
    print(f'Published message ID: {future.result()}')