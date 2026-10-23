import json
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client
from messaging_models import MessagePayload

# Dead-letter topic configuration
DL_TOPIC_ID = 'your-dead-letter-topic-id'
PROJECT_ID = 'your-gcp-project-id'

def send_to_dead_letter(original_msg, error_details: str):
    """Send a failed message (and its metadata) to a Pub/Sub dead-letter topic.

    Args:
        original_msg (Message): The original Pub/Sub message object.
        error_details (str): Description of why processing failed.
    """
    publisher = get_publisher_client()
    dl_payload = {
        "original_message": {
            "message_id": original_msg.message.message_id,
            "data": original_msg.message.data.decode('utf-8'),
            "attributes": original_msg.message.attributes or {}
        },
        "error_details": error_details,
        "timestamp": __import__('datetime').datetime.utcnow().isoformat() + 'Z'
    }
    dl_data = json.dumps(dl_payload).encode('utf-8')
    publisher.publish(DL_TOPIC_ID, data=dl_data)
    print(f"Sent failed message to dead-letter topic: {dl_payload}")

# Example usage stub\nif __name__ == '__main__':
    # In real code you would receive `original_msg` from error handling flow
    fake_msg = type('FakeMessage', (), {
        'message': type('FakePubSubMessage', (), {
            'message_id': 'fake-id-001',
            'data': json.dumps({"event_id": "test-dl"}).encode(),
            'attributes': {'retry_count': '3'}
        })
    })
    send_to_dead_letter(fake_msg, "payload validation failed")
