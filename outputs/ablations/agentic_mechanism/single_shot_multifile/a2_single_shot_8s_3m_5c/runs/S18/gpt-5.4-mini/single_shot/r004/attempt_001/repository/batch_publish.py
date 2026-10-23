import json
from typing import Any, Dict, Iterable, List

from google.cloud import pubsub_v1

from messaging_client import get_publish_topic_path, get_publisher_client
from messaging_models import normalize_batch_item


def batch_publish(messages: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    publisher = get_publisher_client()
    topic_path = get_publish_topic_path()
    message_ids: List[str] = []
    normalized_messages: List[Dict[str, Any]] = []
    for index, item in enumerate(messages):
        payload = normalize_batch_item(item, index=index)
        normalized_messages.append(payload)
        data = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
        future = publisher.publish(topic_path, data=data, item_id=str(payload.get("item_id", index)), batch_index=str(index))
        message_ids.append(future.result())
    return {"message_ids": message_ids, "topic_path": topic_path, "messages": normalized_messages}
