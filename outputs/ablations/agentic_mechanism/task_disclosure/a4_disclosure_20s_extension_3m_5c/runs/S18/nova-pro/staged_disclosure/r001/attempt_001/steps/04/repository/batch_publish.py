import boto3

def publish_batch(topic_arn, messages):
    sns = boto3.client('sns')
    publish_entries = []
    for message in messages:
        publish_entries.append({'Id': message['Id'], 'Message': message['Message'], 'MessageAttributes': message.get('MessageAttributes', {})})
    response = sns.publish_batch(TopicArn=topic_arn, PublishBatchRequestEntries=publish_entries)
    return response

if __name__ == '__main__':\n    topic_arn = 'arn:aws:sns:REGION:ACCOUNT_ID:TOPIC_NAME'\n    messages = [\n        {'Id': '1', 'Message': 'Hello, world!'},\n        {'Id': '2', 'Message': 'Hello, again!'},\n    ]
    response = publish_batch(topic_arn, messages)
    print(response)