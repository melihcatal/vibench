from messaging_client import get_sqs_client


def dead_letter(queue_url: str, payload: str, reason: str) -> str:
    sqs = get_sqs_client()
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=payload,
        MessageAttributes={
            "reason": {"DataType": "String", "StringValue": reason},
            "destination": {"DataType": "String", "StringValue": "dead-letter"},
        },
    )
    return response["MessageId"]
