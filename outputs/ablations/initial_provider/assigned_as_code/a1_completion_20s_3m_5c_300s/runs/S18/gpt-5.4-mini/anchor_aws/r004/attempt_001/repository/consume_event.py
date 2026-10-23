import json

from messaging_client import sqs_client, load_config


def consume_event(config=None):
    config = load_config(config)
    client = sqs_client(config)
    response = client.receive_message(QueueUrl=config["queue_url"], MaxNumberOfMessages=1, WaitTimeSeconds=0)
    messages = response.get("Messages", [])
    if not messages:
        return {"message": None}
    message = messages[0]
    body = message.get("Body")
    try:
        body = json.loads(body)
    except Exception:
        pass
    return {"message_id": message.get("MessageId"), "receipt_handle": message.get("ReceiptHandle"), "body": body}
