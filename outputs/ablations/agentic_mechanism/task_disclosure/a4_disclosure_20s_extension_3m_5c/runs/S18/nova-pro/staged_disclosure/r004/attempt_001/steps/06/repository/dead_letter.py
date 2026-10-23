import boto3

# Initialize a session using Amazon SNS
sns = boto3.client('sns')

# SNS topic ARN
topic_arn = 'arn:aws:sns:REGION:ACCOUNT_ID:TOPIC_NAME'

# Dead-letter queue ARN
dlq_arn = 'arn:aws:sqs:REGION:ACCOUNT_ID:DEAD_LETTER_QUEUE_NAME'

def send_message(message):
    try:
        response = sns.publish(
            TopicArn=topic_arn,
            Message=message
        )
        print(f'Message sent: {response}')
    except Exception as e:
        print(f'Failed to send message: {e}')
        send_to_dead_letter(message)

def send_to_dead_letter(message):
    try:
        response = sns.publish(
            TopicArn=dlq_arn,
            Message=message
        )
        print(f'Message sent to dead-letter queue: {response}')
    except Exception as e:
        print(f'Failed to send message to dead-letter queue: {e}')

# Example usage
send_message('This is a test message.')