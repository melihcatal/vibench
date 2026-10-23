from google.cloud import pubsub_v1

project_id = 'your-project-id'
topic_id = 'your-topic-id'

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def publish_event(data):
    data['timestamp'] = str(datetime.datetime.utcnow())
    data_json = json.dumps(data).encode('utf-8')
    future = publisher.publish(topic_path, data_json)
    result = future.result()
    print(f'Published message ID: {result}')

if __name__ == '__main__':
    event_data = {
        'event_type': 'example',
        'event_data': 'This is a test event'
    }
    publish_event(event_data)