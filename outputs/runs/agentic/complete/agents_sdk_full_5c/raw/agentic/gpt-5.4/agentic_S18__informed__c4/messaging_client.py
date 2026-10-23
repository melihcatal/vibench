from __future__ import annotations

import json
import os
from typing import Dict, Optional

import boto3
from botocore.config import Config

from messaging_models import MessageEnvelope, normalize_attributes


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL", "")
SQS_DEAD_LETTER_QUEUE_URL = os.getenv("SQS_DEAD_LETTER_QUEUE_URL", "")


_session = boto3.session.Session(region_name=AWS_REGION)
_config = Config(retries={"max_attempts": 5, "mode": "standard"})


def get_sqs_client():
    return _session.client("sqs", config=_config)


def get_translate_client():
    return _session.client("translate", config=_config)


def get_comprehend_client():
    return _session.client("comprehend", config=_config)


def get_bedrock_runtime_client():
    return _session.client("bedrock-runtime", config=_config)


def get_dynamodb_resource():
    return _session.resource("dynamodb", config=_config)


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def resolve_queue_url(explicit_queue_url: Optional[str] = None) -> str:
    queue_url = explicit_queue_url or SQS_QUEUE_URL
    if not queue_url:
        raise ValueError("SQS queue URL is required via argument or SQS_QUEUE_URL")
    return queue_url


def resolve_dead_letter_queue_url(explicit_queue_url: Optional[str] = None) -> str:
    queue_url = explicit_queue_url or SQS_DEAD_LETTER_QUEUE_URL
    if not queue_url:
        raise ValueError("Dead-letter queue URL is required via argument or SQS_DEAD_LETTER_QUEUE_URL")
    return queue_url


def sqs_message_attributes(attributes: Optional[Dict[str, str]]) -> Dict[str, Dict[str, str]]:
    normalized = normalize_attributes(attributes)
    return {
        key: {"StringValue": value, "DataType": "String"}
        for key, value in normalized.items()
    }


def encode_envelope(envelope: MessageEnvelope) -> Dict[str, object]:
    return {
        "MessageBody": json.dumps(envelope.body, separators=(",", ":"), ensure_ascii=False),
        "MessageAttributes": sqs_message_attributes(envelope.attributes),
    }
