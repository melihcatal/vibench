import json
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_config, get_publisher
from messaging_models import MessageEnvelope, build_batch_result, normalize_batch_payloads, normalize_attributes

def batch_publish(messages, topic_path=None):
    cfg = get_pubsub_config()
    publisher = get_publisher(cfg)
    topic = topic_path or cfg.topic_path
    batch = normalize_batch_payloads(messages)
    results = []
    for item in batch:
        envelope = MessageEnvelope(payload=item['payload'], attributes=normalize_attributes(item.get('attributes')), message_id=item.get('id'))
        data = json.dumps(envelope.to_dict(), ensure_ascii=False).encode('utf-8')
        message_id = publisher.publish(topic, data, **envelope.attributes).result(timeout=30)
        results.append({'input_id': item.get('id'), 'message_id': message_id})
    return build_batch_result(provider='google-cloud-pubsub', topic=topic, results=results)

if __name__ == '__main__':
    print(json.dumps(batch_publish([{'id':'1','payload':{'event':'a'}}]), ensure_ascii=False))
