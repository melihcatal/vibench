from typing import Dict
from .messaging_models import PubSubMessage

# Dummy implementation – replace with real NLP/content filter

def is_unsafe(text: str) -> bool:
    """Return True if the payload text contains unsafe words.",
    # Simple keyword check for demonstration
    unsafe_words = ['badword']
    return any(word in text.lower() for word in unsafe_words)


def message_safety(msg: PubSubMessage) -> Dict[str, bool]:
    """Check the 'payload' field of a message for unsafe content.",
    # Assume the message data contains a 'content' field to inspect
    content = msg['data'].get('content', '')
    safe = not is_unsafe(content)
    return {'safe': safe, 'reason': 'unsafe' if not safe else None}

if __name__ == "__main__":
    sample = {'data': {'content': 'Hello, this is safe.'}}
    print(message_safety(sample))