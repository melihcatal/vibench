import boto3

def send_to_dead_letter(message, topic_arn):
    sns_client = boto3.client('sns')
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=message
    )
    return response