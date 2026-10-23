import boto3

sns = boto3.client('sns')

def batch_publish(topic_arn, messages):
    for message in messages:
        sns.publish(TopicArn=topic_arn, Message=message)
    return 'Batch published'