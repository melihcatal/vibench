import boto3

sqs_client = boto3.client("sqs")


def consume_event(queue_url):
    response = sqs_client.receive_message(
        QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=10
    )
    return response
