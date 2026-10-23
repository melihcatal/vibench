import os
import json
import boto3

def send_to_dead_letter_queue(dlq_url: str, message_body: dict, original_message_id: str = None) -> dict:
    """Sends a failed message to an AWS SQS Dead-Letter Queue."""
    sqs_client = boto3.client(
        "sqs",
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    try:
        attributes = {}
        if original_message_id:
            attributes["OriginalMessageId"] = {
                "DataType": "String",
                "StringValue": original_message_id
            }

        response = sqs_client.send_message(
            QueueUrl=dlq_url,
            MessageBody=json.dumps(message_body),
            MessageAttributes=attributes
        )
        return {"dlq_message_id": response["MessageId"], "status": "success"}
    except Exception as e:
        return {"status": "error", "details": str(e)}

if __name__ == "__main__":
    # Example Usage (requires AWS_REGION and SQS_DLQ_URL environment variables)
    # Ensure AWS credentials are configured
    # dlq_url = os.environ.get("SQS_DLQ_URL")
    # if not dlq_url:
    #     print("SQS_DLQ_URL environment variable not set.")
    # else:
    #     failed_event = {"error": "processing_failed", "original_payload": {"user_id": "failed_1"}}
    #     result = send_to_dead_letter_queue(dlq_url, failed_event, "original-msg-id-123")
    #     print(f"DLQ send result: {result}")
    pass
