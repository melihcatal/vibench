from __future__ import annotations

from typing import Iterable, List, Optional

from messaging_client import get_publisher_client, get_topic_path
from messaging_models import MessagePayload, MessageResult


def batch_publish(messages: Iterable[MessagePayload], topic: Optional[str] = None) -> MessageResult:
    publisher = get_publisher_client()
    topic_path = get_topic_path(topic)
    publish_futures: List = []
    local_ids: List[str] = []
    for item in messages:
        attrs = dict(item.attributes)
        attrs.setdefault("client_message_id", item.message_id)
        if item.ordering_key:
            future = publisher.publish(topic_path, item.to_json_bytes(), ordering_key=item.ordering_key, **attrs)
        else:
            future = publisher.publish(topic_path, item.to_json_bytes(), **attrs)
        publish_futures.append(future)
        local_ids.append(item.message_id)

    published_ids = [future.result() for future in publish_futures]
    return MessageResult(
        provider="google-cloud-pubsub",
        destination=topic_path,
        message_ids=published_ids,
        status="batch-published",
        details={"client_message_ids": local_ids, "count": len(published_ids)},
    )
