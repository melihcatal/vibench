import json

# [SAME-SCENARIO] dead_letter.py
# Sends failed messages to a dead-letter SQS queue named 'my-message-queue-dlq'

from messaging_client import get_sqs_client


def send_to_dead_letter(original_message: dict, client=None) -> dict:
    """Send a failed message payload to a dead-letter SQS queue and get the response.

    Args:
        original_message (dict): The original message dict including Body and ReceiptHandle.
        client (Optional[any]): An already-instantiated SQS client; if None, a new client is created.
    Returns:
        dict: SQS send_message response or an error message.
    """
    if client is None:
        client = get_sqs_client()
    dlq_url = "https://sqs.us-east-1.amazonaws.com/123456789012/my-message-queue-dlq"  # example ARN/path
    # Reuse the original body; you could add metadata if needed
    message_body = json.dumps(original_message)
    try:
        response = client.send_message(QueueUrl=dlq_url, MessageBody=message_body)
        return response
    except Exception as e:
        return {"error": str(e)}
