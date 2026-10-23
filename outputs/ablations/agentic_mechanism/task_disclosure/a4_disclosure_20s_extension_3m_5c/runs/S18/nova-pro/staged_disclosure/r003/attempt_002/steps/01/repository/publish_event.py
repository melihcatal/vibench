import boto3
import json

def publish_event(topic_arn, message):
    sns_client = boto3.client('sns')
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=json.dumps({'default': json.dumps(message)}),
        MessageStructure='json'
    )
    return response

if __name__ == '__main__':
    topic_arn = 'arn:aws:sns:REGION:ACCOUNT_ID:TOPIC_NAME'
    message = {'key1': 'value1', 'key2': 'value2'}
    response = publish_event(topic_arn, message)
    print(response)