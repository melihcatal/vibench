import os
import json
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_client
from messaging_models import BatchEventRequest

publisher = get_pubsub_client()
topic_path = publisher.topic_path(os.getenv("GOOGLE_CLOUD_PROJECT"), os.getenv("PUBSUB_TOPIC_ID", "events-topic"))

def batch_publish(events: list[dict]) -> list[str]: 
    batch = publisher.batch()
    requests = [BatchEventRequest(**event) for event in events]
    
    for request in requests:
        batch.publish(
            topic_path,
            data=json.dumps(request.dict()).encode("utf-8"),
            message_id=request.event_id
        )
    
    return batch.commit()