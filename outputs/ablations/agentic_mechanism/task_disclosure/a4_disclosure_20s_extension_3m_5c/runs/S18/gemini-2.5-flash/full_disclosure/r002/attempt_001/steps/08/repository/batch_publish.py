from google.cloud import pubsub_v1

def publish_batch_messages(project_id: str, topic_id: str, messages: list[tuple[str, dict | None]]):
    """Publishes a batch of messages to a Pub/Sub topic.

    Args:
        project_id: The Google Cloud project ID.
        topic_id: The Pub/Sub topic ID.
        messages: A list of tuples, where each tuple contains (message_data, attributes).
                  message_data is a string, and attributes is an optional dictionary.
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    futures = []
    for message_data, attributes in messages:
        data = message_data.encode("utf-8")
        if attributes:
            future = publisher.publish(topic_path, data, **attributes)
        else:
            future = publisher.publish(topic_path, data)
        futures.append(future)

    for future in futures:
        # Blocks until the message is published.
        message_id = future.result()
        print(f"Published message with ID: {message_id}")

