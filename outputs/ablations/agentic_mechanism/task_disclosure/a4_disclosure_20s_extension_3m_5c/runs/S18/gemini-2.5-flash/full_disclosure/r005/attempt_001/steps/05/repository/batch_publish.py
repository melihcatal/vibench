from google.cloud import pubsub_v1

def publish_batch_messages(project_id: str, topic_id: str, messages: list[dict]):
    """Publishes a batch of messages to a Pub/Sub topic.

    Args:
        project_id: The Google Cloud project ID.
        topic_id: The Pub/Sub topic ID.
        messages: A list of dictionaries, where each dictionary represents a message
                  and can contain 'data' (str or bytes) and 'attributes' (dict).
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    futures = []
    for message_data in messages:
        data = message_data.get("data", "").encode("utf-8") if isinstance(message_data.get("data"), str) else message_data.get("data")
        attributes = message_data.get("attributes", {})

        # The publish method can take arbitrary keyword arguments for attributes.
        future = publisher.publish(topic_path, data, **attributes)
        futures.append(future)

    for future in futures:
        # Wait for all the message futures to resolve
        message_id = future.result()
        print(f"Published message with ID: {message_id}")

    print(f"Published {len(messages)} messages to {topic_path}")
