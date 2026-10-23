from messaging_client import get_publisher_client, get_project_id
from messaging_models import create_event_payload

def publish_event(topic_id: str, data: dict, event_type: str):
    project_id = get_project_id()
    publisher = get_publisher_client()
    topic_path = publisher.topic_path(project_id, topic_id)

    event_payload = create_event_payload(data, event_type)
    future = publisher.publish(topic_path, event_payload.encode("utf-8"))
    print(f"Published message ID: {future.result()}")
    publisher.api.transport.close()


if __name__ == "__main__":
    # Example usage (replace with your topic_id and actual data)
    example_topic_id = "your-topic-id"
    example_data = {"message": "Hello, Google Cloud Pub/Sub!", "source": "example_app"}
    example_event_type = "greeting"
    publish_event(example_topic_id, example_data, example_event_type)
