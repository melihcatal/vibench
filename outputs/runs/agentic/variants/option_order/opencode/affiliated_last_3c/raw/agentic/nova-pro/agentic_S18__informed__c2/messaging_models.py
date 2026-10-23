from typing import Dict


def normalize_message(message: Dict) -> Dict:
    return {
        "Message": message.get("Message", ""),
        "MessageAttributes": message.get("MessageAttributes", {}),
    }
