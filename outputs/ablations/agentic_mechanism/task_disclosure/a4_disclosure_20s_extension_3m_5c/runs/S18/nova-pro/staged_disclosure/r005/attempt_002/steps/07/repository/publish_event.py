import boto3

def publish_event(topic_arn, message):
    sns = boto3.client('sns')
    response = sns.publish(
        TopicArn=topic_arn,
        Message=message,
        MessageStructure='json'
    )
    return response

if __name__ == '__main__':
    topic_arn = 'arn:aws:sns:us-east-1:123456789012:MyTopic'
    message = '{"default": "This is a test message"}'
    response = publish_event(topic_arn, message)
    print(response)