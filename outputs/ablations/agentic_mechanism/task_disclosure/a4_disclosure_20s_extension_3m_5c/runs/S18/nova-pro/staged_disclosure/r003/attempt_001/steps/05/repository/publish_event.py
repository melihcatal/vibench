import json
import boto3

def publish_event(topic_arn, message):
    sns = boto3.client('sns')
    response = sns.publish(
        TopicArn=topic_arn,
        Message=json.dumps({'default': json.dumps(message)})
    )
    print(response)

if __name__ == '__main__':
    topic_arn = 'arn:aws:sns:REGION:ACCOUNT_ID:TOPIC_NAME'
    message = {'key1': 'value1', 'key2': 'value2'}
    publish_event(topic_arn, message)