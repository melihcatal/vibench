import boto3

def send_to_dead_letter(message_body):
    sqs = boto3.client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/MyDeadLetterQueue'
    response = sqs.send_message(QueueUrl=queue_url, MessageBody=message_body)
    return response

if __name__ == '__main__':
    message_body = 'This is a failed message'
    response = send_to_dead_letter(message_body)
    print(response)