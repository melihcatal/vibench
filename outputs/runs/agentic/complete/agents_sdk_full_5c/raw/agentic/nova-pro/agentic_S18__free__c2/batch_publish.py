import boto3

sns_client = boto3.client('sns')

def batch_publish(topic_arn, messages):
    for message in messages:
        sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            MessageAttributes={
                'AttributeName': {
                    'DataType': 'String',
                    'StringValue': 'AttributeValue'
                }
            }
        )
    return 'Batch published'