import json
from messaging_client import get_messaging_client


def send_to_dead_letter(failed_message, dead_letter_topic):
    """Send a failed message to a dead-letter destination.

    Uses Amazon SNS/SQS via the boto3 SDK.
    Required environment variables:
        AWS_ACCESS_KEY_ID
        AWS_SECRET_ACCESS_KEY
    """
    client = get_messaging_client()
    # Serialize the failed message payload
    message_body = json.dumps(failed_message)
    # Publish to the dead-letter SNS topic (or SQS queue if using the SQS client)
    response = client.publish(
        TopicArn=dead_letter_topic, Message=message_body, MessageAttributes={}
    )
    return response
