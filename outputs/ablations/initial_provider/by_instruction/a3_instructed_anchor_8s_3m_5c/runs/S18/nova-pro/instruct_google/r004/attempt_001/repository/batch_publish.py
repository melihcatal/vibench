from google.cloud import pubsub_v1

def batch_publish(project_id, topic_id, messages):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    future_results = [publisher.publish(topic_path, json.dumps(message).encode('utf-8')) for message in messages]
    return [future.result() for future in future_results]