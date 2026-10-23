import boto3

def publish_batch(topic_arn, messages):
    sns = boto3.client('sns')
    publish_batch_request_entries = []
    for message in messages:
        publish_batch_request_entries.append({
            'Id': message['Id'],
            'Message': message['Message']
        })
    response = sns.publish_batch(
        TopicArn=topic_arn,
        PublishBatchRequestEntries=publish_batch_request_entries
    )
    return response

# Example usage
topic_arn = 'arn:aws:sns:us-east-1:123456789012:MyTopic'
messages = [
    {
        'Id': '1',
        'Message': 'Hello from message 1'
    },
    {
        'Id': '2',
        'Message': 'Hello from message 2'
    }
]
response = publish_batch(topic_arn, messages)
print(response)