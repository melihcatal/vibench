from google.cloud import pubsub_v1

project_id = "your-project-id"
topic_id = "your-topic-id"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def batch_publish(messages):
    futures = publisher.publish(topic_path, messages)
    print(f'Published batch message IDs: {[future.result() for future in futures]}')