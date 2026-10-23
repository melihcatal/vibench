from google.cloud import pubsub_v1

project_id = "your-project-id"
topic_id = "your-dead-letter-topic-id"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def dead_letter(data):
    data = bytes(data, encoding='utf8')
    future = publisher.publish(topic_path, data)
    print(f'Published dead letter message ID: {future.result()}')