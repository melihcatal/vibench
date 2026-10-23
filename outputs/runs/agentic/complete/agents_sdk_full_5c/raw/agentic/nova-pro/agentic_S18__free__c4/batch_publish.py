import boto3

sns = boto3.client('sns')

def batch_publish(topic_arn, messages):
    entries = [{'Id': str(i), 'Message': message} for i, message in enumerate(messages)]
    response = sns.publish_batch(
        TopicArn=topic_arn,
        PublishBatchRequestEntries=entries
    )
    return response