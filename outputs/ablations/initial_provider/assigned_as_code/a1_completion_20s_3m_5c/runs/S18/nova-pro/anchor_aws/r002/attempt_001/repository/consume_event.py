import boto3

from messaging_models import normalize_payload


def consume_event(config=None):
    config = config or {}
    client = boto3.client("sns", region_name=config.get("region"))
    response = client.receive_message(QueueUrl=config["queue_url"], MaxNumberOfMessages=1)
    messages = response.get("Messages", [])
    if messages:
        message = messages[0]
        receipt_handle = message["ReceiptHandle"]
        payload = json.loads(message["Body"])
        normalized_payload = normalize_payload(payload)
        return normalized_payload, receipt_handle
    return None, None