from google.cloud import pubsub_v1

def publish_batch_messages(project_id: str, topic_id: str, messages: list[dict]):
    """Publishes a batch of messages with IDs or attributes to a Google Cloud Pub/Sub topic.

    Args:
        project_id: The Google Cloud project ID.
        topic_id: The Pub/Sub topic ID.
        messages: A list of dictionaries, where each dictionary represents a message.
                  Each message can have 'data' (str), 'message_id' (str, optional),
                  and 'attributes' (dict, optional).
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    futures = []
    for message in messages:
        data = message.get('data', '').encode('utf-8')
        message_id = message.get('message_id')
        attributes = message.get('attributes')

        if message_id:
            if attributes:
                future = publisher.publish(topic_path, data, message_id=message_id, **attributes)
            else:
                future = publisher.publish(topic_path, data, message_id=message_id)
        else:
            if attributes:
                future = publisher.publish(topic_path, data, **attributes)
            else:
                future = publisher.publish(topic_path, data)
        futures.append(future)

    for future in futures:
        # Blocks until the message is published.
        future.result()
