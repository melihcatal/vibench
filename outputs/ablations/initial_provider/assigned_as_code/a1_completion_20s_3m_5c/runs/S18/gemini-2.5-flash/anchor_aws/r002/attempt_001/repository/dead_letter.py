import json
from messaging_client import get_sqs_client

def dead_letter(queue_url, message_body, config=None):
    config = config or {}
    sqs_client = get_sqs_client(config.get("region"))
    response = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message_body)
    )
    return {"message_id": response["MessageId"]}
