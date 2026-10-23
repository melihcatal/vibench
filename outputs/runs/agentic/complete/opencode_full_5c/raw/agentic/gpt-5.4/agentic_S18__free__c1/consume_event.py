from __future__ import annotations

from messaging_client import queue_url, sqs_client
from messaging_models import ConsumedMessage, safe_json_loads


def consume_event(delete_after_receive: bool = False) -> ConsumedMessage | None:
    client = sqs_client()
    response = client.receive_message(
        QueueUrl=queue_url(),
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10,
        MessageAttributeNames=["All"],
        AttributeNames=["All"],
    )
    messages = response.get("Messages", [])
    if not messages:
        return None
    message = messages[0]
    if delete_after_receive:
        client.delete_message(
            QueueUrl=queue_url(), ReceiptHandle=message["ReceiptHandle"]
        )
    attrs = {
        key: value.get("StringValue", "")
        for key, value in message.get("MessageAttributes", {}).items()
    }
    body_text = message["Body"]
    body = safe_json_loads(body_text)
    if "Message" in body and isinstance(body["Message"], str):
        raw_body = body["Message"]
        body = safe_json_loads(raw_body)
    else:
        raw_body = body_text
    return ConsumedMessage(
        provider="aws_sqs",
        subscription=queue_url(),
        receipt_handle=message["ReceiptHandle"],
        message_id=message["MessageId"],
        body=body,
        attributes=attrs,
        raw_body=raw_body,
    )
