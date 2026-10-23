import json
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_config, get_subscriber
from messaging_models import build_consume_result, normalize_received_message

def consume_event(subscription_path=None, timeout=10):
    cfg = get_pubsub_config()
    subscriber = get_subscriber(cfg)
    subscription = subscription_path or cfg.subscription_path
    response = subscriber.pull(subscription=subscription, max_messages=1, timeout=timeout)
    if not response.received_messages:
        return build_consume_result(provider='google-cloud-pubsub', subscription=subscription, message=None)
    received = response.received_messages[0]
    normalized = normalize_received_message(received)
    subscriber.acknowledge(subscription=subscription, ack_ids=[received.ack_id])
    return build_consume_result(provider='google-cloud-pubsub', subscription=subscription, message=normalized)

if __name__ == '__main__':
    print(json.dumps(consume_event(), ensure_ascii=False))
