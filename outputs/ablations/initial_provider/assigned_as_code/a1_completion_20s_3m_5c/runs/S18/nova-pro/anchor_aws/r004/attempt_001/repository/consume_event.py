import boto3

from messaging_client import get_sqs_client


def consume_event():
    client = get_sqs_client()
    response = client.receive_message(QueueUrl=get_sqs_client().get_queue_url(QueueName='my-queue')['QueueUrl'], MaxNumberOfMessages=1)
    messages = response.get('Messages', [])
    if messages:
        return json.loads(messages[0]['Body'])
    return None