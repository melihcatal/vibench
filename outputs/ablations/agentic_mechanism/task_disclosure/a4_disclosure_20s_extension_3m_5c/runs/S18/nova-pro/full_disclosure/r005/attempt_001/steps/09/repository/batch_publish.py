import boto3

def publish_batch(topic_arn, messages):
    sns = boto3.client('sns')
    publish_entries = []
    for message in messages:
        publish_entries.append({
            'Id': message['Id'],
            'Message': message['Message'],
            'MessageAttributes': message.get('MessageAttributes', {})
        })
    response = sns.publish_batch(
        TopicArn=topic_arn,
        PublishBatchRequestEntries=publish_entries
    )
    return response

# Example usage:
# topic_arn = 'arn:aws:sns:REGION:ACCOUNT_ID:TOPIC_NAME'
# messages = [
#     {
#         'Id': 'msg-001',
#         'Message': 'Hello, World!',
#         'MessageAttributes': {
#             'AttributeName': {
#                 'DataType': 'String',
#                 'StringValue': 'AttributeValue'
#             }
#         }
#     }
# ]
# publish_batch(topic_arn, messages)