import json
from messaging_client import resolve_topic_arn, sns_client, message_attributes
from messaging_models import PublishRequest, PublishResponse, normalize_message_body


def publish_event(payload, topic_arn=None, subject=None, attributes=None):
    request = PublishRequest(
        topic_arn=resolve_topic_arn(topic_arn),
        payload=payload,
        subject=subject,
        message_attributes=attributes,
    )
    response = sns_client().publish(
        TopicArn=request.topic_arn,
        Message=normalize_message_body(request.payload),
        Subject=request.subject or "event",
        MessageAttributes=message_attributes(request.message_attributes),
    )
    return PublishResponse(message_id=response["MessageId"], metadata={k: v for k, v in response.items() if k != "MessageId"})


def main():
    event = json.loads(input())
    result = publish_event(event)
    print(json.dumps({"message_id": result.message_id, "metadata": result.metadata}))


if __name__ == "__main__":
    main()
