import os
import json
import boto3

def consume_event(queue_url: str, max_messages: int = 1) -> list:
    """Consumes one or more messages from an AWS SQS queue."""
    sqs_client = boto3.client(
        "sqs",
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    messages = []
    try:
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=max_messages,
            WaitTimeSeconds=10 # Long polling
        )
        if "Messages" in response:
            for message in response["Messages"]:
                # Assume the message body is JSON
                try:
                    body = json.loads(message["Body"])
                except json.JSONDecodeError:
                    body = message["Body"] # Fallback if not JSON
                
                messages.append({
                    "receipt_handle": message["ReceiptHandle"],
                    "message_id": message["MessageId"],
                    "body": body,
                    "attributes": message.get("Attributes", {})
                })
                # For demonstration, we're not deleting here.
                # In a real app, process and then delete.
                # sqs_client.delete_message(
                #     QueueUrl=queue_url,
                #     ReceiptHandle=message["ReceiptHandle"]
                # )
        return messages
    except Exception as e:
        print(f"Error consuming messages: {e}")
        return []

if __name__ == "__main__":
    # Example Usage (requires AWS_REGION and SQS_QUEUE_URL environment variables)
    # Ensure AWS credentials are configured
    # queue_url = os.environ.get("SQS_QUEUE_URL")
    # if not queue_url:
    #     print("SQS_QUEUE_URL environment variable not set.")
    # else:
    #     consumed_messages = consume_event(queue_url)
    #     if consumed_messages:
    #         for msg in consumed_messages:
    #             print(f"Consumed message ID: {msg['message_id']}, Body: {msg['body']}")
    #     else:
    #         print("No messages to consume.")
    pass
