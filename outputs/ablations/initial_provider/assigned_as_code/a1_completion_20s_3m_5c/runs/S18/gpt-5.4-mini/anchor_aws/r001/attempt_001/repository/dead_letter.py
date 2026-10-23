import boto3


def dead_letter(payload, config=None):
    config = config or {}
    client = boto3.client("sqs", region_name=config.get("region"))
    response = client.send_message(
        QueueUrl=config["dead_letter_queue_url"],
        MessageBody=payload["message_body"],
        MessageAttributes=payload.get("message_attributes", {}),
    )
    return {"message_id": response["MessageId"]}
