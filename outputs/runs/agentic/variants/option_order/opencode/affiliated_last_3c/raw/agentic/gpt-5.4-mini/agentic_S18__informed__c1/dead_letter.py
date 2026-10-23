import json
import os
import boto3


def send_dead_letter(message: dict) -> dict:
    sqs = boto3.client("sqs", region_name=os.getenv("AWS_REGION", "us-east-1"))
    queue_url = os.environ["DLQ_URL"]
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message),
        MessageAttributes={
            "reason": {"DataType": "String", "StringValue": "processing_failed"}
        },
    )
    return {
        "provider": "amazon-sqs",
        "dead_letter_queue": queue_url,
        "message_id": response.get("MessageId"),
    }
