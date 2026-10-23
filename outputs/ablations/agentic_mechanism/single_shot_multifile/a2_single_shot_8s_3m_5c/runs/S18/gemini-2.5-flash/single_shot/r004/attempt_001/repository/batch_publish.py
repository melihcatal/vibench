import os
import json
from google.cloud.pubsub_v1 import futures
from messaging_client import PubSubClientHelper
from messaging_models import EventMessage, BatchPublishResult

def publish_batch_events(events: list[EventMessage]) -> BatchPublishResult:
    client_helper = PubSubClientHelper()
    publisher = client_helper.get_publisher_client()
    topic_id = os.environ.get("GCP_PUBSUB_TOPIC_ID")
    if not topic_id:
        raise ValueError("GCP_PUBSUB_TOPIC_ID environment variable not set.")

    topic_path = client_helper.get_topic_path(topic_id)

    future_results = []
    for event in events:
        data = json.dumps(event['data']).encode("utf-8")
        attributes = event.get('attributes', {})
        attributes['event_id'] = event['event_id']

        future = publisher.publish(topic_path, data, **attributes)
        future_results.append(future)

    successful_ids = []
    failed_errors = []

    for future in future_results:
        try:
            message_id = future.result(timeout=60) # Wait for each message to be published
            successful_ids.append(message_id)
        except futures.TimeoutError:
            failed_errors.append(f"Message publishing timed out.")
        except Exception as e:
            failed_errors.append(f"Message publishing failed: {e}")

    return BatchPublishResult(
        success=not bool(failed_errors),
        message_ids=successful_ids,
        errors=failed_errors if failed_errors else None
    )
