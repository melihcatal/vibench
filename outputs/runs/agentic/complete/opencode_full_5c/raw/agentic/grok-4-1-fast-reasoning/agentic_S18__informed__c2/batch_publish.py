import json
from messaging_client import get_topic_path, get_publisher_client
from messaging_models import MessageEvent


def batch_publish(events: list[MessageEvent], topic_id: str = None) -> list[str]:
    topic_path = get_topic_path(topic_id)
    publisher = get_publisher_client()
    elements = []
    for event in events:
        data = json.dumps(event.payload).encode("utf-8")
        element = {"data": data}
        if event.attributes:
            element["attributes"] = event.attributes
        elements.append(element)
    api_futures = publisher.publish_messages(topic_path, elements)
    return [future.result() for future in api_futures]
