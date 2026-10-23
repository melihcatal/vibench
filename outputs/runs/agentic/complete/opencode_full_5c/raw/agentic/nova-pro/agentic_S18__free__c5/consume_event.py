import boto3


def consume_event(queue_url):
    sqs_client = boto3.client("sqs")
    response = sqs_client.receive_message(
        QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=10
    )
    if "Messages" in response:
        return response["Messages"][0]
    return None
