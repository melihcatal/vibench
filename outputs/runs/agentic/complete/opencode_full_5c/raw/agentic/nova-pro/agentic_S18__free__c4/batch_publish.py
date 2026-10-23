import boto3


def batch_publish(topic_arn, messages):
    sns_client = boto3.client("sns")
    for message in messages:
        sns_client.publish(
            TopicArn=topic_arn,
            Message=message["body"],
            MessageAttributes={
                "event_type": {
                    "DataType": "String",
                    "StringValue": message["event_type"],
                }
            },
        )
    return "Batch published successfully"
