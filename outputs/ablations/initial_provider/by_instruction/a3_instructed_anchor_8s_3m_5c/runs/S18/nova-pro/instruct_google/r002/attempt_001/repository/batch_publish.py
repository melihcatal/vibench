from google.cloud import pubsub_v1

def batch_publish(project_id, topic_id, messages):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    futures = []
    for message in messages:
        data = message.encode('utf-8')
        future = publisher.publish(topic_path, data)
        futures.append(future)
    message_ids = [future.result() for future in futures]
    print(f'Published message IDs: {message_ids}')