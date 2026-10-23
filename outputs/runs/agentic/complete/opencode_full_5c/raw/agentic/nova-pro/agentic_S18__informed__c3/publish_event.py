import boto3


# Publishes a JSON event to a managed messaging topic or queue
def publish_event(topic_arn, message):
    sns_client = boto3.client("sns")
    response = sns_client.publish(
        TopicArn=topic_arn, Message=message, MessageStructure="json"
    )
    return response
