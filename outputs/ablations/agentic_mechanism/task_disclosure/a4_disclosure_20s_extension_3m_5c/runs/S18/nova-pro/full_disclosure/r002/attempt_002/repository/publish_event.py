import json
import boto3

def publish_event(topic_arn, message):
    sns_client = boto3.client('sns')
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=json.dumps({'default': json.dumps(message)}),
        MessageStructure='json'
    )
    return response
