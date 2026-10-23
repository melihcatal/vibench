from google.cloud import pubsub_v1

def consume_event(project_id, subscription_id):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    response = subscriber.pull(subscription_path, max_messages=1)
    return response.received_messages[0].message if response.received_messages else None