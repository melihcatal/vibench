import json

from messaging_client import load_config, publisher_client, topic_path
from messaging_models import BatchRequest, MessageRequest


def batch_publish(messages):
    config = load_config()
    client = publisher_client()
    topic = topic_path(config)
    batch = BatchRequest(messages=[MessageRequest(payload=m) for m in messages])
    message_ids = []
    for request in batch.messages:
        message_ids.append(client.publish(topic, request.to_bytes(), **request.attributes).result())
    return {"message_ids": message_ids}


if __name__ == "__main__":
    print(json.dumps(batch_publish([{"id": "1"}, {"id": "2"}])))
