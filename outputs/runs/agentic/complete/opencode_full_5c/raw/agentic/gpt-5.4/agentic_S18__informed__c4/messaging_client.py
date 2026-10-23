from __future__ import annotations

import json
import os
from typing import Any

import boto3

from messaging_models import ConsumedMessage, MessageEvent, PublishAck, normalize_body


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def get_region_name() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def get_sqs_client():
    return boto3.client("sqs", region_name=get_region_name())


def get_sns_client():
    return boto3.client("sns", region_name=get_region_name())


def get_dynamodb_resource():
    return boto3.resource("dynamodb", region_name=get_region_name())


def get_primary_queue_url() -> str:
    return _required_env("AWS_SQS_QUEUE_URL")


def get_dead_letter_queue_url() -> str:
    return _required_env("AWS_SQS_DEAD_LETTER_QUEUE_URL")


def get_topic_arn() -> str:
    return _required_env("AWS_SNS_TOPIC_ARN")


def get_audit_table_name() -> str:
    return _required_env("AWS_DYNAMODB_AUDIT_TABLE")


def publish_to_sns(event: MessageEvent) -> PublishAck:
    client = get_sns_client()
    response = client.publish(
        TopicArn=get_topic_arn(),
        Message=event.to_json(),
        MessageAttributes={
            key: {"DataType": "String", "StringValue": value}
            for key, value in event.attributes.items()
        },
    )
    return PublishAck(destination=get_topic_arn(), message_id=response["MessageId"])


def publish_batch_to_sqs(entries: list[dict[str, Any]]) -> dict[str, Any]:
    return get_sqs_client().send_message_batch(
        QueueUrl=get_primary_queue_url(), Entries=entries
    )


def receive_one_message(wait_time_seconds: int = 10) -> ConsumedMessage | None:
    response = get_sqs_client().receive_message(
        QueueUrl=get_primary_queue_url(),
        MaxNumberOfMessages=1,
        WaitTimeSeconds=wait_time_seconds,
        MessageAttributeNames=["All"],
        AttributeNames=["All"],
    )
    messages = response.get("Messages", [])
    if not messages:
        return None
    message = messages[0]
    attributes = {
        key: value.get("StringValue", "")
        for key, value in message.get("MessageAttributes", {}).items()
    }
    body = normalize_body(message.get("Body"))
    if "Message" in body and isinstance(body["Message"], str):
        body = normalize_body(body["Message"])
    return ConsumedMessage(
        message_id=message["MessageId"],
        receipt_handle=message["ReceiptHandle"],
        body=body,
        attributes=attributes,
        queue_url=get_primary_queue_url(),
    )


def delete_message(receipt_handle: str) -> dict[str, Any]:
    return get_sqs_client().delete_message(
        QueueUrl=get_primary_queue_url(), ReceiptHandle=receipt_handle
    )


def send_to_dead_letter(
    message: dict[str, Any], attributes: dict[str, str] | None = None
) -> dict[str, Any]:
    return get_sqs_client().send_message(
        QueueUrl=get_dead_letter_queue_url(),
        MessageBody=json.dumps(message, ensure_ascii=False),
        MessageAttributes={
            key: {"DataType": "String", "StringValue": value}
            for key, value in (attributes or {}).items()
        },
    )
