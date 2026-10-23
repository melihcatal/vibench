import boto3

def publish_message(topic_arn, message):
    sns_client = boto3.client('sns')
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=message,
        MessageAttributes={
            'Title': {
                'DataType': 'String',
                'StringValue': 'Test Message'
            }
        }
    )
    return response