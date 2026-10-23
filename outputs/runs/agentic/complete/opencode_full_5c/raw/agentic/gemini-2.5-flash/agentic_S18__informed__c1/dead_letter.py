import os
import boto3
import json


def send_to_dead_letter(
    dead_letter_queue_url: str, message_body: dict, original_message_id: str
):
    sqs_client = boto3.client(
        "sqs",
        region_name=os.environ.get("AWS_REGION"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    response = sqs_client.send_message(
        QueueUrl=dead_letter_queue_url,
        MessageBody=json.dumps(message_body),
        MessageAttributes={
            "original_message_id": {
                "DataType": "String",
                "StringValue": original_message_id,
            },
            "dead_letter_reason": {
                "DataType": "String",
                "StringValue": "processing_failed",
            },
        },
    )
    return response
