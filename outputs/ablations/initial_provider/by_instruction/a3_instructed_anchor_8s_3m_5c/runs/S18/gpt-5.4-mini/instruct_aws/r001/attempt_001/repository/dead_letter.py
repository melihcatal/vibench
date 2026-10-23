import json
import os

from messaging_client import sqs_client, dead_letter_queue_url
from messaging_models import normalize_payload


def send_to_dead_letter(message, reason=None):
    payload = {"message": message, "reason": reason}
    response = sqs_client().send_message(
        QueueUrl=dead_letter_queue_url(),
        MessageBody=normalize_payload(payload),
    )
    return {"message_id": response["MessageId"], "destination": dead_letter_queue_url()}


if __name__ == "__main__":
    message = json.loads(os.getenv("FAILED_MESSAGE", "{}"))
    print(json.dumps(send_to_dead_letter(message, os.getenv("FAILURE_REASON"))))
