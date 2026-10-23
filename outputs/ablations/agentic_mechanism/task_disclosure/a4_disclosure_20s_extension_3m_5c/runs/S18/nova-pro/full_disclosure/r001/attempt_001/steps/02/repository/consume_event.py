from google.cloud import pubsub_v1

def consume_event(project_id, subscription_id):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    response = subscriber.pull(request={
        'subscription': subscription_path,
        'max_messages': 1
    })
    if response.received_messages:
        message = response.received_messages[0]
        ack_id = message.ack_id
        data = message.message.data.decode('utf-8')
        print(f'Received message: {data}')
        subscriber.acknowledge(request={
            'subscription': subscription_path,
            'ack_ids': [ack_id]
        })
    else:
        print('No messages returned.')

# Example usage:
# consume_event('your-project-id', 'your-subscription-id')