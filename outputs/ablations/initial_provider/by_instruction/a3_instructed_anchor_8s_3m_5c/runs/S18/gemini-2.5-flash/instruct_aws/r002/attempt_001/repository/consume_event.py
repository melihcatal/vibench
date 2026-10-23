import boto3
import json
from messaging_client import get_sqs_queue_url
from messaging_models import Message

def consume_event():
    """
    Consumes one message from an AWS SQS queue.
    """
    sqs_client = boto3.client('sqs')
    queue_url = get_sqs_queue_url()

    try:
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10,
            MessageAttributeNames=['All']
        )

        messages = response.get('Messages', [])
        if messages:
            sqs_message = messages[0]
            message = Message.from_sqs_message(sqs_message)
            print(f"Consumed message ID: {message.message_id}")
            print(f"Message body: {message.body}")
            print(f"Message attributes: {message.attributes}")
            
            # For demonstration, we'll just print and then delete it.
            # In a real scenario, you'd process the message before deleting.
            sqs_client.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=sqs_message['ReceiptHandle']
            )
            print(f"Deleted message ID: {message.message_id}")
            return message
        else:
            print("No messages to consume.")
            return None
    except Exception as e:
        print(f"Error consuming message: {e}")
        raise

if __name__ == "__main__":
    consume_event()
