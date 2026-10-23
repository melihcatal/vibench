import boto3

def send_to_dead_letter(message_body, source_queue_url, dead_letter_queue_url):
    sqs = boto3.client('sqs')
    
    # Receive message from the source queue
    response = sqs.receive_message(
        QueueUrl=source_queue_url,
        MaxNumberOfMessages=1,
        MessageAttributeNames=['All'],
        VisibilityTimeout=0,
        WaitTimeSeconds=10
    )
    
    if 'Messages' in response:
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        
        # Send message to the dead-letter queue
        sqs.send_message(
            QueueUrl=dead_letter_queue_url,
            MessageBody=message_body,
            MessageAttributes=message['MessageAttributes']
        )
        
        # Delete message from the source queue
        sqs.delete_message(
            QueueUrl=source_queue_url,
            ReceiptHandle=receipt_handle
        )
    else:
        print('No messages to move to dead-letter queue.')

# Example usage:
# send_to_dead_letter('Failed message', 'https://sqs.us-east-1.amazonaws.com/123456789012/MyQueue', 'https://sqs.us-east-1.amazonaws.com/123456789012/DeadLetterQueue')