import json

import boto3

from messaging_client import get_sns_sqs_client_config


def dead_letter(payload, config=None):
    config = get_sns_sqs_client_config(config)
    client = boto3.client("sqs", region_name=config["region"])
    response = client.send_message(
        QueueUrl=config["dead_letter_queue_url"],
        MessageBody=json.dumps(payload),
        MessageAttributes={
            "source": {"DataType": "String", "StringValue": config.get("source", "pubsub")}
        },
    )
    return {"message_id": response["MessageId"]}
