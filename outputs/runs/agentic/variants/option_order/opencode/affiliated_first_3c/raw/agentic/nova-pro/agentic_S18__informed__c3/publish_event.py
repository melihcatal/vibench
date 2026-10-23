import boto3


def publish_event(topic_arn, message):
    sns_client = boto3.client("sns")
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=message,
        MessageAttributes={
            "EventType": {"DataType": "String", "StringValue": "example_event_type"}
        },
    )
    return response
