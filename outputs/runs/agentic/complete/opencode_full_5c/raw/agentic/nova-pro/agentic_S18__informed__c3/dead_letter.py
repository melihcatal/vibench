import boto3


# Sends failed messages to a dead-letter destination
def dead_letter(queue_url, message):
    sqs_client = boto3.client("sqs")
    response = sqs_client.send_message(QueueUrl=queue_url, MessageBody=message)
    return response
