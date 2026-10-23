import boto3


def summarize_message_processing(message_ids):
    client = boto3.client("sns")
    summary = {"success": 0, "failure": 0}
    for message_id in message_ids:
        try:
            response = client.get_message_attributes(MessageId=message_id)
            summary["success"] += 1
        except client.exceptions.MessageDoesNotExist:
            summary["failure"] += 1
    return summary