import json

from messaging_client import sqs_client, load_config


def dead_letter(payload, config=None):
    config = load_config(config)
    client = sqs_client(config)
    response = client.send_message(QueueUrl=config["dead_letter_queue_url"], MessageBody=json.dumps(payload))
    return {"message_id": response.get("MessageId")}
