import os
import boto3

sns = boto3.client(
    "sns",
    region_name="us-east-1",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def batch_publish(topic_arn, messages):
    response = sns.publish_batch(
        TopicArn=topic_arn,
        PublishBatchRequestEntries=[
            {"Id": str(i), "Message": message} for i, message in enumerate(messages)
        ],
    )
    return response
