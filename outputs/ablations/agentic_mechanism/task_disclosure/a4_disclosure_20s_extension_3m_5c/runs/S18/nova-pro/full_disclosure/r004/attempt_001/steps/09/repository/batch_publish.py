import boto3

def publish_batch(topic_arn, messages):
    sns = boto3.client('sns')
    publish_entries = []
    for message in messages:
        publish_entries.append({
            'Id': message['Id'],
            'Message': message['Message'],
            'MessageAttributes': message.get('Attributes', {}),
        })
    response = sns.publish_batch(
        TopicArn=topic_arn,
        PublishBatchRequestEntries=publish_entries
    )
    return response

# Example usage:
# topic_arn = 'arn:aws:sns:us-east-1:123456789012:my-topic'
# messages = [
#     {'Id': 'msg1', 'Message': 'Hello, world!', 'Attributes': {}},
#     {'Id': 'msg2', 'Message': 'Hello again!', 'Attributes': {'attr1': {'DataType': 'String', 'StringValue': 'value1'}}},
# ]
# response = publish_batch(topic_arn, messages)
# print(response)