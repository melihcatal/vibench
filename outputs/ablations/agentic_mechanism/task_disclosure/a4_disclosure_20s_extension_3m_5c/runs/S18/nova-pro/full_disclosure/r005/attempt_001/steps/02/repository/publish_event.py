import boto3

def publish_event(topic_arn, message):
    sns_client = boto3.client('sns')
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=message,
        MessageStructure='json'
    )
    return response

if __name__ == '__main__'):
    topic_arn = 'arn:aws:sns:us-east-1:123456789012:my-topic'
    message = '{"default": "This is a test message"}'
    response = publish_event(topic_arn, message)
    print(response)