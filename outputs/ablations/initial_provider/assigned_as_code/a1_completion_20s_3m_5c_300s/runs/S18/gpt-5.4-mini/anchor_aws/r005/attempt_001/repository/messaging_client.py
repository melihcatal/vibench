import os

from messaging_models import coerce_message_payload, coerce_message_records


def _get_env(name, default=None):
    value = os.getenv(name)
    return default if value is None or value == "" else value


def get_sns_sqs_client_config(config=None):
    config = dict(config or {})
    return {
        "region": config.get("region") or _get_env("AWS_REGION") or _get_env("AWS_DEFAULT_REGION") or "us-east-1",
        "topic_arn": config.get("topic_arn") or _get_env("SNS_TOPIC_ARN"),
        "queue_url": config.get("queue_url") or _get_env("SQS_QUEUE_URL"),
        "dead_letter_queue_url": config.get("dead_letter_queue_url") or _get_env("SQS_DEAD_LETTER_QUEUE_URL"),
        "wait_time_seconds": int(config.get("wait_time_seconds") or _get_env("SQS_WAIT_TIME_SECONDS", "0")),
        "delete_after_receive": bool(config.get("delete_after_receive", True)),
        "source": config.get("source") or _get_env("MESSAGE_SOURCE", "pubsub"),
    }


def normalize_message_record(payload, raw_message=None):
    return coerce_message_payload(payload, raw_message)


def normalize_batch_items(payload):
    return coerce_message_records(payload)
