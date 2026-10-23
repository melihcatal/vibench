from __future__ import annotations

import os
from typing import Any

import boto3


def aws_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def topic_arn() -> str:
    return os.environ["AWS_SNS_TOPIC_ARN"]


def queue_url() -> str:
    return os.environ["AWS_SQS_QUEUE_URL"]


def dead_letter_queue_url() -> str:
    return os.environ["AWS_SQS_DLQ_URL"]


def dynamodb_table_name() -> str:
    return os.environ["AWS_DYNAMODB_TABLE"]


def sns_client() -> Any:
    return boto3.client("sns", region_name=aws_region())


def sqs_client() -> Any:
    return boto3.client("sqs", region_name=aws_region())


def comprehend_client() -> Any:
    return boto3.client("comprehend", region_name=aws_region())


def translate_client() -> Any:
    return boto3.client("translate", region_name=aws_region())


def bedrock_runtime_client() -> Any:
    return boto3.client("bedrock-runtime", region_name=aws_region())


def dynamodb_resource() -> Any:
    return boto3.resource("dynamodb", region_name=aws_region())
