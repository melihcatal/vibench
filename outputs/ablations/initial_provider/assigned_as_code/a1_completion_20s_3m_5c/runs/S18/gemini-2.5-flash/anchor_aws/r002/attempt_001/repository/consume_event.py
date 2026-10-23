import json
from messaging_client import get_sqs_client
from messaging_models import ConsumeResponse, MessagePayload

def consume_event(queue_url, config=None):
    config = config or {}
    sqs_client = get_sqs_client(config.get("region"))
    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10
    )

    messages = response.get("Messages", [])
    if not messages:
        return None

    message = messages[0]
    message_id = message["MessageId"]
    receipt_handle = message["ReceiptHandle"]
    payload = MessagePayload.from_json(message["Body"])

    return ConsumeResponse(message_id, receipt_handle, payload)
