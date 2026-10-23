import json

from google.cloud import pubsub_v1


def consume_event():
    client = pubsub_v1.SubscriberClient()
    subscription_name = 'projects/{project_id}/subscriptions/{subscription_id}'.format(
        project_id='your-project-id',
        subscription_id='your-subscription-id'
    )
    response = client.pull(request={'subscription': subscription_name, 'max_messages': 1})
    if response.received_messages:
        message = response.received_messages[0]
        ack_id = message.ack_id
        print(f'Received message: {message.message.data.decode()}')
        client.acknowledge(request={'subscription': subscription_name, 'ack_ids': [ack_id]})


def dead_letter(message):
    client = pubsub_v1.PublisherClient()
    topic_name = 'projects/{project_id}/topics/{topic_id}'.format(
        project_id='your-project-id',
        topic_id='your-dead-letter-topic-id'
    )
    future = client.publish(topic_name, message.encode('utf-8'))
    try:
        return {'message_id': future.result(timeout=30)}
    finally:
        client.stop()


def batch_publish(payloads):
    client = pubsub_v1.PublisherClient()
    topic_name = 'projects/{project_id}/topics/{topic_id}'.format(
        project_id='your-project-id',
        topic_id='your-topic-id'
    )
    futures = []
    for payload in payloads:
        future = client.publish(topic_name, json.dumps(payload).encode('utf-8'))
        futures.append(future)
    try:
        message_ids = [future.result(timeout=30) for future in futures]
        return {'message_ids': message_ids}
    finally:
        client.stop()