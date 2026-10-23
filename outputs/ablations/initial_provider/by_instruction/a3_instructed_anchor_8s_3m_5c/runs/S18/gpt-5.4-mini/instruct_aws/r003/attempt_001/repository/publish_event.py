import json

from messaging_client import get_settings, sns_client
from messaging_models import MessageRequest


def publish_event(event):
    settings = get_settings()
    request = MessageRequest(message_id=event.get("id", ""), payload=event, attributes=event.get("attributes"))
    response = sns_client().publish(
        TopicArn=settings["topic_arn"],
        Message=json.dumps(request.to_dict()["payload"]),
        MessageAttributes={k: {"DataType": "String", "StringValue": v} for k, v in (request.attributes or {}).items()},
    )
    return {"ok": True, "provider_message_id": response.get("MessageId", ""), "detail": response}
