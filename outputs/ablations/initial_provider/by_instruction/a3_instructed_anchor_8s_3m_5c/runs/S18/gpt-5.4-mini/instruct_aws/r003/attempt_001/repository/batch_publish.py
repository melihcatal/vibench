import json

from messaging_client import get_settings, sns_client


def batch_publish(events):
    settings = get_settings()
    results = []
    for event in events:
        response = sns_client().publish(
            TopicArn=settings["topic_arn"],
            Message=json.dumps(event),
            MessageAttributes={"message_id": {"DataType": "String", "StringValue": str(event.get("id", ""))}},
        )
        results.append({"id": event.get("id", ""), "provider_message_id": response.get("MessageId", "")})
    return results
