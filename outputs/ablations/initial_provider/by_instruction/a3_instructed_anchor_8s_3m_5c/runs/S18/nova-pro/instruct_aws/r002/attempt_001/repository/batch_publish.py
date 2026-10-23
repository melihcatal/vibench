import boto3

def batch_publish(topic_arn, messages):
    sns = boto3.client('sns')
    response = sns.publish_batch(
        TopicArn=topic_arn,
        PublishBatchRequestEntries=[
            {
                'Id': str(i),
                'Message': message,
            }
            for i, message in enumerate(messages)
        ],
    )
    return response