from __future__ import annotations

from typing import Any
import json
import os

import boto3

from messaging_models import (
    BatchPublishItem,
    ConsumedMessage,
    PublishEventRequest,
    json_dumps,
)


def get_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def sns_client():
    return boto3.client("sns", region_name=get_region())


def sqs_client():
    return boto3.client("sqs", region_name=get_region())


def dynamodb_resource():
    return boto3.resource("dynamodb", region_name=get_region())


def build_sns_attributes(attributes: dict[str, str]) -> dict[str, dict[str, str]]:
    return {
        key: {"DataType": "String", "StringValue": value}
        for key, value in attributes.items()
    }


def publish_to_topic(request: PublishEventRequest) -> dict[str, Any]:
    client = sns_client()
    params: dict[str, Any] = {
        "TopicArn": request.topic_arn,
        "Message": request.as_message(),
        "MessageAttributes": build_sns_attributes(request.attributes),
    }
    if request.subject:
        params["Subject"] = request.subject
    return client.publish(**params)


def publish_batch(topic_arn: str, items: list[BatchPublishItem]) -> dict[str, Any]:
    client = sns_client()
    entries = []
    for item in items:
        entries.append(
            {
                "Id": item.message_id,
                "Message": json_dumps(item.payload),
                "MessageAttributes": build_sns_attributes(item.attributes),
                **({"Subject": item.subject} if item.subject else {}),
            }
        )
    return client.publish_batch(TopicArn=topic_arn, PublishBatchRequestEntries=entries)


def receive_one_message(
    queue_url: str, wait_time_seconds: int = 10
) -> ConsumedMessage | None:
    client = sqs_client()
    response = client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=wait_time_seconds,
        MessageAttributeNames=["All"],
        AttributeNames=["All"],
    )
    messages = response.get("Messages", [])
    if not messages:
        return None
    message = messages[0]
    body_raw = message.get("Body", "{}")
    try:
        envelope = json.loads(body_raw)
    except json.JSONDecodeError:
        envelope = {"Body": body_raw}
    payload = envelope
    if isinstance(envelope, dict) and "Message" in envelope:
        try:
            payload = json.loads(envelope["Message"])
        except (TypeError, json.JSONDecodeError):
            payload = {"text": str(envelope["Message"])}
    return ConsumedMessage(
        message_id=message["MessageId"],
        receipt_handle=message["ReceiptHandle"],
        body=payload if isinstance(payload, dict) else {"value": payload},
        attributes=message.get("Attributes", {}),
        raw=message,
    )


def delete_message(queue_url: str, receipt_handle: str) -> dict[str, Any]:
    return sqs_client().delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)


def send_to_queue(
    queue_url: str, payload: dict[str, Any], attributes: dict[str, str] | None = None
) -> dict[str, Any]:
    params: dict[str, Any] = {
        "QueueUrl": queue_url,
        "MessageBody": json_dumps(payload),
    }
    if attributes:
        params["MessageAttributes"] = {
            key: {"DataType": "String", "StringValue": value}
            for key, value in attributes.items()
        }
    return sqs_client().send_message(**params)
