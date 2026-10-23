import boto3


def publish_event(topic_arn, message):
    sns_client = boto3.client("sns")
    response = sns_client.publish(
        TopicArn=topic_arn, Message=message, MessageStructure="json"
    )
    return response
