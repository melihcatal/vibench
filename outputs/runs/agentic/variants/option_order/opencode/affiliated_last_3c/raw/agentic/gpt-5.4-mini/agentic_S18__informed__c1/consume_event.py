import json
import os
import boto3

from messaging_models import MessageEnvelope


def consume_event() -> dict:
    sqs = boto3.client("sqs", region_name=os.getenv("AWS_REGION", "us-east-1"))
    queue_url = os.environ["SQS_QUEUE_URL"]
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=1,
        MessageAttributeNames=["All"],
    )
    messages = response.get("Messages", [])
    if not messages:
        return {"provider": "amazon-sqs", "subscription": queue_url, "status": "empty"}
    message = messages[0]
    body = json.loads(message["Body"])
    envelope = MessageEnvelope(
        id=message["MessageId"],
        payload=body,
        attributes={
            k: v.get("StringValue", "")
            for k, v in message.get("MessageAttributes", {}).items()
        },
    )
    return {
        "provider": "amazon-sqs",
        "subscription": queue_url,
        "status": "ok",
        "message": envelope.__dict__,
    }
