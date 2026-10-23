import boto3

def publish_event(topic_arn, message):
    sns_client = boto3.client('sns', region_name='us-west-2')
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=message,
        MessageAttributes={'ContentType': {'DataType': 'String', 'StringValue': 'application/json'}}
    )
    return response