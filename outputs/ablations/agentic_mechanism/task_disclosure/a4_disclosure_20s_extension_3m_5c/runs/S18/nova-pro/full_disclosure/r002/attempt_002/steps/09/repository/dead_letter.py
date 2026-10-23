import boto3

def send_to_dead_letter_queue(message_body, queue_url):
    sqs = boto3.client('sqs')
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=message_body
    )
    return response

if __name__ == '__main__':
    message_body = 'This is a failed message.'
    queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/MyDeadLetterQueue'
    response = send_to_dead_letter_queue(message_body, queue_url)
    print(response)