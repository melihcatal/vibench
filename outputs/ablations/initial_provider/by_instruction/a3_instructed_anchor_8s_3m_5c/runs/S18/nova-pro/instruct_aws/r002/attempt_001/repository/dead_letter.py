import boto3

def dead_letter(queue_url, message):
    sqs = boto3.client('sqs')
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=message,
    )
    return response