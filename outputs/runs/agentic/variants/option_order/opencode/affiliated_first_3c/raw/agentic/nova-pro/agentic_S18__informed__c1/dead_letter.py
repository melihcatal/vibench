import boto3


def dead_letter(queue_url, message):
    sqs_client = boto3.client("sqs")
    response = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=message,
        MessageAttributes={
            "Event-Type": {"DataType": "String", "StringValue": "dead-letter"}
        },
    )
    return response
