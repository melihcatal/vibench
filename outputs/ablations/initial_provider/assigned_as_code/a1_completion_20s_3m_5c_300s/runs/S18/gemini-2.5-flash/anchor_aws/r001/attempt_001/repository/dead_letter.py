import json
import boto3
from messaging_client import get_sqs_client

def configure_dead_letter_queue(
    queue_url: str,
    region_name: str,
    dead_letter_queue_arn: str,
    max_receive_count: int
):
    """
    Configures a dead-letter queue for the given SQS queue.
    This function modifies the attributes of an existing SQS queue.
    """
    sqs_client = get_sqs_client(region_name)

    redrive_policy = {
        "deadLetterTargetArn": dead_letter_queue_arn,
        "maxReceiveCount": str(max_receive_count)
    }

    sqs_client.set_queue_attributes(
        QueueUrl=queue_url,
        Attributes={
            'RedrivePolicy': json.dumps(redrive_policy)
        }
    )
    return {"status": "dead-letter queue configured", "queue_url": queue_url, "dead_letter_target_arn": dead_letter_queue_arn}

def get_queue_arn(queue_url: str, region_name: str) -> str:
    sqs_client = get_sqs_client(region_name)
    response = sqs_client.get_queue_attributes(
        QueueUrl=queue_url,
        AttributeNames=['QueueArn']
    )
    return response['Attributes']['QueueArn']
