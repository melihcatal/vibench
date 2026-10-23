import boto3

def publish_batch(topic_arn, messages):
    sns = boto3.client('sns')
    response = sns.publish_batch(
        TopicArn=topic_arn,
        PublishBatchRequestEntries=[
            {
                'Id': message['Id'],
                'Message': message['Message'],
                'MessageAttributes': message.get('MessageAttributes', {})
            } for message in messages
        ]
    )
    return response

# Example usage:
# topic_arn = 'arn:aws:sns:REGION:ACCOUNT_ID:TOPIC_NAME'
# messages = [
#     {
#         'Id': '1',
#         'Message': 'Hello, world!',
#         'MessageAttributes': {
#             'AttributeName': {
#                 'DataType': 'String',
#                 'StringValue': 'AttributeValue'
#             }
#         }
#     }
# ]
# publish_batch(topic_arn, messages)