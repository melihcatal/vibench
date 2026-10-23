from google.cloud import pubsub_v1

def batch_publish(project_id, topic_id, messages):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    for message in messages:
        data = message.get('data', '').encode('utf-8')
        attributes = message.get('attributes', {})
        publisher.publish(topic_path, data, **attributes)

    print(f'Published {len(messages)} messages to {topic_path}')

# Example usage:
# batch_publish('your-project-id', 'your-topic-id', [{'data': 'Hello, World!', 'attributes': {'key1': 'value1'}}, {'data': 'Hello again!', 'attributes': {'key2': 'value2'}}])