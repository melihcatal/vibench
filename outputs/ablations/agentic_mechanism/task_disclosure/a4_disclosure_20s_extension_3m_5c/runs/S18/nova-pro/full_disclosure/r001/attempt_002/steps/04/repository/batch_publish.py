import boto3

def batch_publish(topic_arn, messages):
    sns_client = boto3.client('sns')
    for message in messages:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message['content'],
            MessageAttributes=message.get('attributes', {})
        )
        print(f'Message ID: {response['MessageId']}')

if __name__ == '__main__':
    topic_arn = 'arn:aws:sns:region:account-id:topic-name'
    messages = [
        {"content": "Message 1", "attributes": {}},
        {"content": "Message 2", "attributes": {"AttributeName": {"DataType": "String", "StringValue": "AttributeValue"}}}
    ]
    batch_publish(topic_arn, messages)