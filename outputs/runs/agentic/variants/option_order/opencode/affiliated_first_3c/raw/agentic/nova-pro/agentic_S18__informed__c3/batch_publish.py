import boto3


def batch_publish(topic_arn, messages):
    sns_client = boto3.client("sns")
    response = sns_client.publish_batch(
        TopicArn=topic_arn, PublishBatchRequestEntries=messages
    )
    return response
