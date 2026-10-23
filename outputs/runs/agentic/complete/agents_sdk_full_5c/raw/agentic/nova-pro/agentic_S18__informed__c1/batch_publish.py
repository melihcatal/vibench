import boto3

def batch_publish(topic_arn, messages):
    sns_client = boto3.client('sns', region_name='us-west-2')
    for message in messages:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            MessageAttributes={'ContentType': {'DataType': 'String', 'StringValue': 'application/json'}}
        )
    return response