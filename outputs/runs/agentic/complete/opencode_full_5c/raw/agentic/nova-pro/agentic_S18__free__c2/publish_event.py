import boto3

sns_client = boto3.client("sns")


def publish_event(topic_arn, message):
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=message,
        MessageAttributes={
            "EventSource": {"DataType": "String", "StringValue": "example-source"}
        },
    )
    return response
