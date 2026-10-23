import boto3

def summarize_messages(messages):
    sns_client = boto3.client('sns')
    summary = {
        'total_messages': len(messages),
        'message_ids': [message['MessageId'] for message in messages]
    }
    return summary