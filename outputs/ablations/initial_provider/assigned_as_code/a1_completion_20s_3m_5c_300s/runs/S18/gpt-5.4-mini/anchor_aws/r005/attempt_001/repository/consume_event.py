import json

import boto3

from messaging_client import get_sns_sqs_client_config, normalize_message_record


def consume_event(config=None):
    config = get_sns_sqs_client_config(config)
    client = boto3.client("sqs", region_name=config["region"])
    response = client.receive_message(
        QueueUrl=config["queue_url"],
        MaxNumberOfMessages=1,
        WaitTimeSeconds=config["wait_time_seconds"],
        MessageAttributeNames=["All"],
    )
    messages = response.get("Messages", [])
    if not messages:
        return {"message": None}
    message = messages[0]
    payload = json.loads(message.get("Body", "{}"))
    normalized = normalize_message_record(payload, message)
    if config.get("delete_after_receive", True):
        client.delete_message(QueueUrl=config["queue_url"], ReceiptHandle=message["ReceiptHandle"])
    return normalized
