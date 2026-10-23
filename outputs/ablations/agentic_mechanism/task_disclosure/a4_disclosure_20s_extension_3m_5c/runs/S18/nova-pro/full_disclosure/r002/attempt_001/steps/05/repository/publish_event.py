import boto3

def publish_event(topic_arn, message):
    sns_client = boto3.client('sns')
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=message,
        MessageStructure='json'
    )
    return response

if __name__ == '__main__':
    topic_arn = 'arn:aws:sns:REGION:ACCOUNT_ID:TOPIC_NAME'
    message = '{"default": "Your message here"}'
    response = publish_event(topic_arn, message)
    print(response)