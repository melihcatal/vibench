import json
from google.cloud import pubsub_v1
from messaging_client import get_topic_path
from typing import List, Optional

def batch_publish(events: List[dict], message_ids: Optional[List[str]] = None):
    """
    publishes a batch of messages with IDs or attributes
    """
    topic_path = get_topic_path()
    publisher = pubsub_v1.PublisherClient()
    data_list = [json.dumps(event).encode('utf-8') for event in events]
    futures = []
    mids = message_ids or [None] * len(events)
    for data, mid in zip(data_list, mids):
        kwargs = {'message_id': mid} if mid else {}
        future = publisher.publish(topic_path, data, **kwargs)
        futures.append(future)
    result_ids = [f.result() for f in futures]
    print(f"Batch published: {result_ids}")
    return result_ids