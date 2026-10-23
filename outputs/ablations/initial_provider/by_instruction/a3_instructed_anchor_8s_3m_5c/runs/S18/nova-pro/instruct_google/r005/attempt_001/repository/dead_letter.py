from google.cloud import pubsub_v1

project_id = 'your-project-id'
topic_id = 'your-dead-letter-topic-id'

publisher = pubsub_v1.PublisherClient()
dead_letter_topic_path = publisher.topic_path(project_id, topic_id)

def dead_letter(data):
    data_json = json.dumps(data).encode('utf-8')
    future = publisher.publish(dead_letter_topic_path, data_json)
    result = future.result()
    print(f'Published dead letter message ID: {result}')

if __name__ == '__main__':
    failed_message = {
        'original_message': 'This is a failed message',
        'failure_reason': 'Processing error'
    }
    dead_letter(failed_message)