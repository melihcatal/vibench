import boto3

def publish_event(topic_arn, message):
    sns = boto3.client('sns')
    response = sns.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject='Test SNS Message'
    )
    return response

if __name__ == '__main__':
    topic_arn = 'arn:aws:sns:REGION:ACCOUNT_ID:TOPIC_NAME'
    message = '{"event": "test"}'
    response = publish_event(topic_arn, message)
    print(response)