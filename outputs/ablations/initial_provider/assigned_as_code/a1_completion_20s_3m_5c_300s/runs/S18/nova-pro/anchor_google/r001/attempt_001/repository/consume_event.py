import json
from messaging_client import get_sns_client
from messaging_models import Message

def consume_event(topic_arn):
    client = get_sns_client()
    response = client.subscribe(TopicArn=topic_arn, Protocol='sqs', Endpoint='https://sqs.us-east-1.amazonaws.com/123456789012/MyQueue')
    subscription_arn = response['SubscriptionArn']
    sqs_client = boto3.client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/MyQueue'
    messages = sqs_client.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=20)
    if 'Messages' in messages:
        message = messages['Messages'][0]
        return Message.from_sqs(message)
    return None