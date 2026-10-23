from messaging_client import get_publisher_client, get_project_id
from messaging_models import create_event_payload
from typing import List, Dict

def batch_publish_events(topic_id: str, messages: List[Dict]):
    project_id = get_project_id()
    publisher = get_publisher_client()
    topic_path = publisher.topic_path(project_id, topic_id)

    futures = []
    for msg_data in messages:
        event_type = msg_data.get("event_type", "default_event")
        data = msg_data.get("data", {})
        event_payload = create_event_payload(data, event_type)
        futures.append(publisher.publish(topic_path, event_payload.encode("utf-8")))

    for future in futures:
        print(f"Published message ID: {future.result()}")
    publisher.api.transport.close()


if __name__ == "__main__":
    # Example usage (replace with your topic_id and actual data)
    example_topic_id = "your-topic-id"
    example_messages = [
        {"event_type": "order_created", "data": {"order_id": "123", "amount": 100.0}},
        {"event_type": "user_signed_up", "data": {"user_id": "abc", "email": "test@example.com"}}
    ]
    batch_publish_events(example_topic_id, example_messages)
