import boto3
import json

def batch_publish_events(topic_arn: str, messages: list[dict]):
    sns_client = boto3.client('sns')  # AWS SDK import
    entries = []
    for i, message in enumerate(messages):
        entries.append({
            'Id': str(i),
            'Message': json.dumps(message),
            'MessageStructure': 'json'
        })
    response = sns_client.publish_batch(
        TopicArn=topic_arn,
        PublishBatchRequestEntries=entries
    )
    return response
