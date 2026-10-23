import boto3


def message_summary(messages):
    sqs_client = boto3.client("sqs")
    summary = {"total": len(messages), "success": 0, "failure": 0}
    for message in messages:
        try:
            sqs_client.delete_message(
                QueueUrl="your-queue-url", ReceiptHandle=message["ReceiptHandle"]
            )
            summary["success"] += 1
        except ClientError as e:
            summary["failure"] += 1
    return summary
