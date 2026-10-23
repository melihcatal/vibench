from messaging_client import get_subscriber, get_subscription_path
from messaging_models import parse_pubsub_message


def consume_event(project_id, subscription_id, timeout=10):
    client = get_subscriber()
    sub_path = get_subscription_path(project_id, subscription_id)
    response = client.pull(subscription=sub_path, max_messages=1, timeout=timeout)
    if not response.received_messages:
        return {"message": None, "subscription": sub_path}
    received = response.received_messages[0]
    parsed = parse_pubsub_message(received.message)
    client.acknowledge(subscription=sub_path, ack_ids=[received.ack_id])
    return {"message": parsed, "subscription": sub_path, "ack_id": received.ack_id}
