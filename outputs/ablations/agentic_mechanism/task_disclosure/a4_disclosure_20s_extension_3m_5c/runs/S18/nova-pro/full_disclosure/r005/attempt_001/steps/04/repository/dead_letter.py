import boto3

def send_to_dead_letter(message_body, queue_url):
    sqs = boto3.client('sqs')
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=message_body
    )
    return response