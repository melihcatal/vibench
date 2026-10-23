import boto3

sqs_client = boto3.client('sqs')

def dead_letter(queue_url, message):
    response = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=message
    )
    return response