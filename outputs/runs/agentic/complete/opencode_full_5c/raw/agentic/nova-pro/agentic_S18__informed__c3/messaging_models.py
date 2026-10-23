from typing import Dict


# Define local request, response, and normalization helpers for Pub/Sub Messaging
def normalize_message(message: Dict):
    return {
        "MessageId": message["MessageId"],
        "Message": message["Message"],
        "TopicArn": message["TopicArn"],
    }
