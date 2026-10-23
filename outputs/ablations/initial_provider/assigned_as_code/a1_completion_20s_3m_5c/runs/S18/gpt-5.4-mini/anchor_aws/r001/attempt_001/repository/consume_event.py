import boto3


def consume_event(config=None):
    config = config or {}
    client = boto3.client("sqs", region_name=config.get("region"))
    response = client.receive_message(
        QueueUrl=config["queue_url"],
        MaxNumberOfMessages=1,
        WaitTimeSeconds=config.get("wait_time_seconds", 0),
        VisibilityTimeout=config.get("visibility_timeout", 30),
    )
    messages = response.get("Messages", [])
    if not messages:
        return {"message": None}
    message = messages[0]
    return {
        "message_id": message.get("MessageId"),
        "receipt_handle": message.get("ReceiptHandle"),
        "body": message.get("Body"),
        "attributes": message.get("Attributes", {}),
    }
