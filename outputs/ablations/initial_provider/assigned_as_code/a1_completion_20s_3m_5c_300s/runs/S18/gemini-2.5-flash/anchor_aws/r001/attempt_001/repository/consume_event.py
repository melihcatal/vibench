import json
import os

import boto3

from messaging_models import Message, ConsumeResponse
from messaging_client import get_sqs_client

def consume_event(queue_url: str, region_name: str, max_number_of_messages: int = 1, wait_time_seconds: int = 5) -> ConsumeResponse:
    sqs_client = get_sqs_client(region_name)
    
    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=max_number_of_messages,
        WaitTimeSeconds=wait_time_seconds,
        MessageAttributeNames=['All']
    )

    messages = []
    for msg in response.get("Messages", []):
        body = json.loads(msg["Body"])
        # SNS messages wrap the actual message in a 'Message' field
        # SQS messages directly contain the payload if not from SNS
        actual_message_body = json.loads(body["Message"]) if "Message" in body and "TopicArn" in body else body
        
        message_attributes = {}
        if "MessageAttributes" in msg:
            for attr_name, attr_value in msg["MessageAttributes"].items():
                if "StringValue" in attr_value:
                    message_attributes[attr_name] = attr_value["StringValue"]
                elif "BinaryValue" in attr_value:
                    message_attributes[attr_name] = attr_value["BinaryValue"]

        messages.append(Message(
            id=msg["MessageId"],
            body=actual_message_body,
            attributes=message_attributes
        ))
        
        # Delete the message after processing
        sqs_client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=msg["ReceiptHandle"]
        )

    return ConsumeResponse(messages=messages)
