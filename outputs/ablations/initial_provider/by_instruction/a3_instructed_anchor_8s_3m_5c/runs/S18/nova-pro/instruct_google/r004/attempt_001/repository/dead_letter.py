from google.cloud import pubsub_v1

def dead_letter(project_id, topic_id, data):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    data = json.dumps(data).encode('utf-8')
    publisher.publish(topic_path, data=data)