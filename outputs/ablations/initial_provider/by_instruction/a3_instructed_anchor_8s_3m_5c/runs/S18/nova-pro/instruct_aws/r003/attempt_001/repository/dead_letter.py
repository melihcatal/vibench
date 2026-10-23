import boto3

def send_to_dead_letter(queue_url, message):
    sqs_client = boto3.client('sqs')
    response = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=message
    )
    return response