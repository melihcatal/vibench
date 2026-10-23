import boto3

def batch_publish(topic_arn, messages):
    sns_client = boto3.client('sns')
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=str(messages),
        MessageStructure='json'
    )
    return response