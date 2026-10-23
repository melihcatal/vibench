import json
from concurrent import futures
from messaging_client import get_publisher_client, PUBLISH_TOPIC_ID
from messaging_models import PubsubMessage, BatchPublishRequest, BatchPublishResponse


def publish_batch_of_events(request: BatchPublishRequest) -> BatchPublishResponse:
    """Publishes a batch of JSON events to a Google Cloud Pub/Sub topic."""
    publisher = get_publisher_client()
    topic_path = publisher.topic_path(publisher.project, PUBLISH_TOPIC_ID)

    futures_list = []
    for message in request.messages:
        data = json.dumps(message.data).encode("utf-8")
        future = publisher.publish(topic_path, data, **message.attributes)
        futures_list.append(future)

    # Wait for all messages in the batch to be published
    message_ids = [f.result() for f in futures.as_completed(futures_list)]

    return BatchPublishResponse(message_ids=message_ids)
