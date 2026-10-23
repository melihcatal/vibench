from google.cloud import pubsub_v1

def publish_batch_messages(project_id, topic_id, messages):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    for message in messages:
        data = message.get('data', '').encode('utf-8')
        attributes = message.get('attributes', {})
        publisher.publish(topic_path, data, **attributes)

    print(f'Published {len(messages)} messages to {topic_path}')

if __name__ == '__main__':
    project_id = 'your-project-id'
    topic_id = 'your-topic-id'
    messages = [
        {
            'data': 'Message 1',
            'attributes': {'attribute1': 'value1'}
        },
        {
            'data': 'Message 2',
            'attributes': {'attribute2': 'value2'}
        }
    ]
    publish_batch_messages(project_id, topic_id, messages)