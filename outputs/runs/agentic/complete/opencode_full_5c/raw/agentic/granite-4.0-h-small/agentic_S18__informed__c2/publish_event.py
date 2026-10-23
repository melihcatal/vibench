import json
from messaging_client import get_messaging_client


def publish_event(topic, payload, message_id=None, attributes=None):
    """Publish a JSON event to a managed messaging topic.

    Uses Alibaba Cloud Message Service (MNS) via the alibabacloud_mns SDK.
    Required environment variables:
        ALIBABA_CLOUD_ACCESS_KEY_ID
        ALIBABA_CLOUD_ACCESS_KEY_SECRET
    """
    client = get_messaging_client()
    # Alibaba MNS expects a message body as string; we send JSON string
    message_body = json.dumps(payload)
    # If message_id is provided, set it as a custom attribute
    if message_id:
        attributes = attributes or {}
        attributes["MessageId"] = message_id
    # Publish the message
    response = client.publish_message(
        topic_name=topic, message_body=message_body, message_attributes=attributes
    )
    return response
