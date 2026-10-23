import boto3

sns_client = boto3.client("sns")


def message_summary(topic_arn):
    response = sns_client.list_subscriptions_by_topic(TopicArn=topic_arn)
    return response
