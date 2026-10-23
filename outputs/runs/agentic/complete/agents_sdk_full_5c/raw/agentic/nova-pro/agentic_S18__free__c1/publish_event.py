import boto3

sns = boto3.client('sns')

def publish_event(topic_arn, message):
    response = sns.publish(TopicArn=topic_arn, Message=message)
    return response