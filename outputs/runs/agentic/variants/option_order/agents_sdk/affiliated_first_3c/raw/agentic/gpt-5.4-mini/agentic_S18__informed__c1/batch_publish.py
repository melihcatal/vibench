from __future__ import annotations

from typing import Any, Dict, Iterable, List
import json
import uuid

from messaging_client import get_client, load_config, build_message
from messaging_models import BatchPublishRequest, BatchPublishResponse, MessageEnvelope, PublishResult


def batch_publish(messages: Iterable[Dict[str, Any]]) -> BatchPublishResponse:
    config = load_config()
    envelopes = [MessageEnvelope.from_mapping(message) for message in messages]
    servicebus_messages = [build_message(env.to_json(), env.id, env.content_type, **env.attributes) for env in envelopes]
    with get_client() as client:
        sender = client.get_topic_sender(topic_name=config.topic_name)
        with sender:
            sender.send_messages(servicebus_messages)
    return BatchPublishResponse(results=[PublishResult(message_id=env.id, succeeded=True, detail=config.topic_name) for env in envelopes])


if __name__ == "__main__":
    data = [
        {"id": str(uuid.uuid4()), "type": "batch.item", "body": {"n": 1}},
        {"id": str(uuid.uuid4()), "type": "batch.item", "body": {"n": 2}},
    ]
    response = batch_publish(data)
    print(json.dumps([{"message_id": r.message_id, "succeeded": r.succeeded} for r in response.results]))
