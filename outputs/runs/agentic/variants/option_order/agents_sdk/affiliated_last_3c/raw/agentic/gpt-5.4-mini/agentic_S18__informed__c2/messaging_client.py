from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

import boto3
from botocore.client import BaseClient

from messaging_models import BatchPublishRequest, ConsumeResponse, DeadLetterRequest, MessageEnvelope, PublishRequest, normalize_attributes


@dataclass
class MessagingConfig:
    region_name: str
    topic_arn: str
    queue_url: str
    dead_letter_queue_url: str


def load_config() -> MessagingConfig:
    return MessagingConfig(
        region_name=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
        topic_arn=os.environ.get("SNS_TOPIC_ARN", ""),
        queue_url=os.environ.get("SQS_QUEUE_URL", ""),
        dead_letter_queue_url=os.environ.get("SQS_DLQ_URL", ""),
    )


def build_sns_client(config: MessagingConfig) -> BaseClient:
    return boto3.client("sns", region_name=config.region_name)


def build_sqs_client(config: MessagingConfig) -> BaseClient:
    return boto3.client("sqs", region_name=config.region_name)


def publish_json(client: BaseClient, request: PublishRequest) -> Dict[str, Any]:
    return client.publish(
        TopicArn=request.topic_name,
        Message=json.dumps(request.envelope.payload),
        MessageAttributes={
            k: {"DataType": "String", "StringValue": v}
            for k, v in normalize_attributes(request.envelope.attributes).items()
        },
    )


def publish_batch(client: BaseClient, request: BatchPublishRequest) -> Dict[str, Any]:
    entries = [
        {
            "Id": envelope.message_id,
            "Message": json.dumps(envelope.payload),
            "MessageAttributes": {
                k: {"DataType": "String", "StringValue": v}
                for k, v in normalize_attributes(envelope.attributes).items()
            },
        }
        for envelope in request.envelopes
    ]
    return client.publish_batch(TopicArn=request.topic_name, PublishBatchRequestEntries=entries)


def receive_one(client: BaseClient, queue_url: str) -> Optional[ConsumeResponse]:
    response = client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        MessageAttributeNames=["All"],
        WaitTimeSeconds=1,
    )
    messages = response.get("Messages", [])
    if not messages:
        return None
    message = messages[0]
    payload = json.loads(message.get("Body", "{}"))
    attributes = {
        name: value.get("StringValue", "")
        for name, value in message.get("MessageAttributes", {}).items()
    }
    return ConsumeResponse(
        message_id=message.get("MessageId", ""),
        payload=payload,
        attributes=attributes,
        ack_id=message.get("ReceiptHandle"),
    )


def send_dead_letter(client: BaseClient, request: DeadLetterRequest) -> Dict[str, Any]:
    return client.send_message(
        QueueUrl=request.destination,
        MessageBody=json.dumps(
            {
                "original_message_id": request.original_message_id,
                "reason": request.reason,
                "payload": request.payload,
                "attributes": request.attributes,
            }
        ),
        MessageAttributes={
            "original_message_id": {"DataType": "String", "StringValue": request.original_message_id},
            "reason": {"DataType": "String", "StringValue": request.reason},
        },
    )
