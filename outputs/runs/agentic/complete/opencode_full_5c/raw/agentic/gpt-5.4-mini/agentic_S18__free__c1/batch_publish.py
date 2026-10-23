from messaging_client import encode_json, publisher_client, topic_path
from messaging_models import BatchPublishRequest


def batch_publish(request: BatchPublishRequest) -> list[str]:
    client = publisher_client()
    topic = topic_path(request.topic)
    futures = []
    for message in request.messages:
        futures.append(
            client.publish(topic, encode_json(message.data), **message.attributes)
        )
    return [future.result() for future in futures]
