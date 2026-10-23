from messaging_client import get_sqs_client
from messaging_models import ConsumeResult


def consume_event(queue_url: str) -> ConsumeResult:
    sqs = get_sqs_client()
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=0,
        MessageAttributeNames=["All"],
    )
    messages = response.get("Messages", [])
    if not messages:
        return ConsumeResult(message_id="", receipt_handle=None, payload="", provider="aws-sqs")
    message = messages[0]
    attrs = {k: v.get("StringValue", "") for k, v in message.get("MessageAttributes", {}).items()}
    return ConsumeResult(message_id=message["MessageId"], receipt_handle=message.get("ReceiptHandle"), payload=message.get("Body", ""), attributes=attrs, provider="aws-sqs")
