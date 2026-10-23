import os
import json
import boto3

def batch_publish_events(topic_arn: str, events: list) -> dict:
    """Publishes a batch of JSON events to an AWS SNS topic."""
    sns_client = boto3.client(
        "sns",
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    
    # SNS PublishBatch supports up to 10 messages per request
    # Each entry needs an Id, Message, and optional MessageAttributes/MessageStructure
    entries = []
    for i, event_data in enumerate(events):
        entry = {
            "Id": event_data.get("id", str(i)), # Use provided ID or generate one
            "Message": json.dumps(event_data["payload"]),
            "MessageStructure": 'json'
        }
        if "attributes" in event_data:
            sns_attributes = {}
            for k, v in event_data["attributes"].items():
                sns_attributes[k] = {"DataType": "String", "StringValue": str(v)}
            entry["MessageAttributes"] = sns_attributes
        entries.append(entry)

    results = {"successful": [], "failed": []}
    if not entries:
        return results

    try:
        response = sns_client.publish_batch(
            TopicArn=topic_arn,
            PublishBatchRequestEntries=entries
        )
        results["successful"] = response.get("Successful", [])
        results["failed"] = response.get("Failed", [])
        return results
    except Exception as e:
        return {"status": "error", "details": str(e)}

if __name__ == "__main__":
    # Example Usage (requires AWS_REGION and SNS_TOPIC_ARN environment variables)
    # Ensure AWS credentials are configured
    # topic_arn = os.environ.get("SNS_TOPIC_ARN")
    # if not topic_arn:
    #     print("SNS_TOPIC_ARN environment variable not set.")
    # else:
    #     batch_events = [
    #         {"id": "msg1", "payload": {"type": "order_created", "order_id": "A1"}},
    #         {"id": "msg2", "payload": {"type": "product_viewed", "product_id": "P5"}, "attributes": {"user_segment": "premium"}},
    #         {"id": "msg3", "payload": {"type": "cart_updated", "user_id": "U100"}}
    #     ]
    #     result = batch_publish_events(topic_arn, batch_events)
    #     print(f"Batch publish result: {result}")
    pass
