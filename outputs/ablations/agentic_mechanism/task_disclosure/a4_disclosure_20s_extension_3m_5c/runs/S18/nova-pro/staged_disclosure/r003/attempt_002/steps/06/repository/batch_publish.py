import boto3

def publish_batch_messages(topic_arn, messages):
    sns_client = boto3.client('sns')
    response = sns_client.publish_batch(
        TopicArn=topic_arn,
        PublishBatchRequestEntries=[
            {
                'Id': message['Id'],
                'Message': message['Message']
            } for message in messages
        ]
    )
    return response

# Example usage
topic_arn = 'arn:aws:sns:REGION:ACCOUNT_ID:TOPIC_NAME'
messages = [
    {
        'Id': '1',
        'Message': 'Hello, world!'
    },
    {
        'Id': '2',
        'Message': 'Hello, again!'
    }
]

response = publish_batch_messages(topic_arn, messages)
print(response)