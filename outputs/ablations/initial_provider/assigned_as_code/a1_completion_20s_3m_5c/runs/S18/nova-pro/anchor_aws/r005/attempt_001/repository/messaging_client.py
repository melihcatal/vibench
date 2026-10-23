import boto3

def batch_publish_messages(topic_arn, messages):
    sns_client = boto3.client('sns')
    response = sns_client.publish_batch(
        TopicArn=topic_arn,
        PublishBatchRequestEntries=[
            {
                'Id': str(i),
                'Message': message,
                'MessageAttributes': {
                    'Title': {
                        'DataType': 'String',
                        'StringValue': 'Test Message'
                    }
                }
            } for i, message in enumerate(messages)
        ]
    )
    return response