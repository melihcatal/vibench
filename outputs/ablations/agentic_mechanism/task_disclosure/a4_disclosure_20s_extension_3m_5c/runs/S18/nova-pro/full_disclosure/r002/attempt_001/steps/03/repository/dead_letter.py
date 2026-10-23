import boto3

def send_to_dead_letter(queue_url, message_body):
    sqs = boto3.client('sqs')
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=message_body
    )
    return response

if __name__ == '__main__':
    dead_letter_queue_url = 'https://sqs.REGION.amazonaws.com/ACCOUNT_ID/DeadLetterQueue'
    failed_message = 'This is a failed message.'
    response = send_to_dead_letter(dead_letter_queue_url, failed_message)
    print(response)