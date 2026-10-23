import json
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_config, get_publisher
from messaging_models import MessageEnvelope, build_dead_letter_result, normalize_attributes

def send_dead_letter(payload, reason, attributes=None, dead_letter_topic=None):
    cfg = get_pubsub_config()
    publisher = get_publisher(cfg)
    topic = dead_letter_topic or cfg.dead_letter_topic
    envelope = MessageEnvelope(payload=payload, attributes=normalize_attributes(attributes), metadata={'reason': reason})
    data = json.dumps(envelope.to_dict(), ensure_ascii=False).encode('utf-8')
    message_id = publisher.publish(topic, data, dead_letter_reason=reason, **envelope.attributes).result(timeout=30)
    return build_dead_letter_result(provider='google-cloud-pubsub', topic=topic, message_id=message_id, reason=reason)

if __name__ == '__main__':
    print(json.dumps(send_dead_letter({'event':'failed'}, 'processing_error'), ensure_ascii=False))
