import json
import os
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_config, get_publisher
from messaging_models import MessageEnvelope, build_publish_result, normalize_attributes

def publish_event(payload, attributes=None, topic_path=None):
    cfg = get_pubsub_config()
    publisher = get_publisher(cfg)
    topic = topic_path or cfg.topic_path
    envelope = MessageEnvelope(payload=payload, attributes=normalize_attributes(attributes))
    data = json.dumps(envelope.to_dict(), ensure_ascii=False).encode('utf-8')
    future = publisher.publish(topic, data, **envelope.attributes)
    message_id = future.result(timeout=30)
    return build_publish_result(provider='google-cloud-pubsub', topic=topic, message_id=message_id)

if __name__ == '__main__':
    sample = json.loads(os.environ.get('MESSAGE_PAYLOAD', '{"event":"created"}'))
    print(json.dumps(publish_event(sample), ensure_ascii=False))
