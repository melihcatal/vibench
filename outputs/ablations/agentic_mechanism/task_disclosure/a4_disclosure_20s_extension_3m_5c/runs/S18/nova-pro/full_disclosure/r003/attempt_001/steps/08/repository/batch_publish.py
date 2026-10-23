import boto3

def publish_batch(topic_arn, messages):
    sns_client = boto3.client('sns')
    publish_batch_request_entries = []
    for message in messages:
        publish_batch_request_entries.append({
            'Id': message['Id'],
            'Message': message['Message']
        })
    response = sns_client.publish_batch(
        TopicArn=topic_arn,
        PublishBatchRequestEntries=publish_batch_request_entries
    )
    return response

if __name__ == '__main__'):
    topic_arn = 'arn:aws:sns:us-east-1:123456789012:my-topic'
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
    response = publish_batch(topic_arn, messages)
    print(response)