import boto3

def summarize_message_processing_results(topic_arn, message):
    sns_client = boto3.client('sns')
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject='Message Processing Summary'
    )
    return response