import boto3

def publish_event(topic_arn, message):
    sns = boto3.client('sns')
    response = sns.publish(
        TopicArn=topic_arn,
        Message=message,
    )
    return response