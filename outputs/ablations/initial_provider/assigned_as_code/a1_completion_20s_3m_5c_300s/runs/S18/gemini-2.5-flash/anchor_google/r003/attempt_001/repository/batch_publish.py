from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, get_project_id, get_topic_path
from messaging_models import normalize_message_payload


def batch_publish(messages, config=None):
    config = config or {}
    project_id = config.get("project_id", get_project_id())
    topic_id = config["topic_id"]

    publisher = get_publisher_client()
    topic_path = get_topic_path(project_id, topic_id)

    futures = []
    for msg in messages:
        data = normalize_message_payload(msg["event"])
        attributes = msg.get("attributes", {})
        futures.append(publisher.publish(topic_path, data, **attributes))

    results = []
    for future in futures:
        try:
            results.append({"message_id": future.result(timeout=30)})
        except Exception as e:
            results.append({"error": str(e)})
    
    publisher.stop()
    return results
