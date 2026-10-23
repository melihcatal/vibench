import boto3


def batch_publish(messages, config=None):
    config = config or {}
    sns = boto3.client('sns', region_name=config['region'])
    topic_arn = config['topic_arn']
    publish_batch_request_entries = [
        {
            'Id': str(uuid.uuid4()),
            'Message': json.dumps(message),
            'MessageAttributes': {
                'MessageId': {
                    'StringValue': str(uuid.uuid4()),
                    'DataType': 'String'
                }
            }
        } for message in messages
    ]
    response = sns.publish_batch(
        TopicArn=topic_arn,
        PublishBatchRequestEntries=publish_batch_request_entries
    )
    return response['Successful'] + response['Failed']