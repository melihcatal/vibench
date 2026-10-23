import json

from messaging_client import sqs_client, sqs_queue_url
from messaging_models import parse_json_payload


def consume_event():
    response = sqs_client().receive_message(
        QueueUrl=sqs_queue_url(),
        MaxNumberOfMessages=1,
        WaitTimeSeconds=0,
        MessageAttributeNames=["All"],
    )
    messages = response.get("Messages", [])
    if not messages:
        return None
    message = messages[0]
    body = parse_json_payload(message.get("Body"))
    return {"message": body, "receipt_handle": message.get("ReceiptHandle"), "message_id": message.get("MessageId")}


if __name__ == "__main__":
    print(json.dumps(consume_event()))
