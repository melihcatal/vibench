import os

import boto3


def load_config(config=None):
    config = config or {}
    return {
        "region": config.get("region") or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        "topic_arn": config.get("topic_arn") or os.getenv("SNS_TOPIC_ARN"),
        "queue_url": config.get("queue_url") or os.getenv("SQS_QUEUE_URL"),
        "dead_letter_queue_url": config.get("dead_letter_queue_url") or os.getenv("SQS_DLQ_URL"),
        "table_name": config.get("table_name") or os.getenv("AUDIT_TABLE_NAME"),
    }


def sns_client(config=None):
    config = load_config(config)
    return boto3.client("sns", region_name=config["region"])


def sqs_client(config=None):
    config = load_config(config)
    return boto3.client("sqs", region_name=config["region"])


def dynamodb_resource(config=None):
    config = load_config(config)
    return boto3.resource("dynamodb", region_name=config["region"])
