import boto3

sqs = boto3.client('sqs')

def dead_letter(queue_url, message_body):
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=message_body
    )
    return response