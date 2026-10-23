import boto3
from messaging_client import get_sns_client
from messaging_models import PublishRequest, PublishResponse, normalize_payload


def publish_event(request: PublishRequest) -> PublishResponse:
    sns = get_sns_client()
    response = sns.publish(
        TopicArn=request.topic_arn,
        Message=normalize_payload(request.payload),
        Subject=request.subject or "message-event",
        MessageAttributes={
            key: {"DataType": "String", "StringValue": value}
            for key, value in request.attributes.items()
        },
    )
    return PublishResponse(message_id=response["MessageId"], sequence_number=response.get("SequenceNumber"), provider="aws-sns")
