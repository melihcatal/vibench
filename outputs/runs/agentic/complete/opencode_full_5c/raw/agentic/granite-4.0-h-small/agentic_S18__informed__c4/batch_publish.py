import os
from messaging_client import get_pubsub_client, serialize_event


def batch_publish(topic_name, events):
    """Publish a list of events as a batch.

    The client implementation decides whether to send multiple publish calls or a single batch call.
    """
    client = get_pubsub_client()
    responses = []
    for ev in events:
        payload = serialize_event(ev)
        resp = client.publish(topic_name, payload)
        responses.append(resp)
    print(f"Batch published {len(events)} events, responses: {responses}")
