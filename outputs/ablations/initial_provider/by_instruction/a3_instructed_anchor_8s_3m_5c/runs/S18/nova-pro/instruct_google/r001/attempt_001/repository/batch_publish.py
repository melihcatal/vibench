from google.cloud import pubsub_v1

def batch_publish(project_id, topic_id, messages):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    futures = []
    for data in messages:
        data = data.encode('utf-8')
        futures.append(publisher.publish(topic_path, data))
    message_ids = [future.result() for future in futures]
    print(f'Published message IDs: {message_ids}')