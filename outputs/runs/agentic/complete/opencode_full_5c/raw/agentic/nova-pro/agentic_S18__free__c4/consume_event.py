import boto3


def consume_event(queue_url):
    sqs_client = boto3.client("sqs")
    response = sqs_client.receive_message(
        QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=10
    )
    if "Messages" in response:
        message = response["Messages"][0]
        receipt_handle = message["ReceiptHandle"]
        sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
        return message["Body"]
    return None
