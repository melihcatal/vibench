import boto3


def summarize_message_processing(message_id, status):
    client = boto3.client('sns')
    topic_arn = 'arn:aws:sns:us-east-1:123456789012:message-processing-summary'
    client.publish(
        TopicArn=topic_arn,
        Message=f'Message ID: {message_id}, Status: {status}'
    )