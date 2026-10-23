from google.cloud import pubsub_v1

project_id = 'your-project-id'
topic_id = 'your-topic-id'

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def batch_publish(messages):
    futures = []
    for message in messages:
        message['timestamp'] = str(datetime.datetime.utcnow())
        data_json = json.dumps(message).encode('utf-8')
        future = publisher.publish(topic_path, data_json)
        futures.append(future)
    results = [future.result() for future in futures]
    print(f'Published message IDs: {results}')

if __name__ == '__main__':
    batch_messages = [
        {
            'event_type': 'example',
            'event_data': 'This is a batch test event 1'
        },
        {
            'event_type': 'example',
            'event_data': 'This is a batch test event 2'
        }
    ]
    batch_publish(batch_messages)