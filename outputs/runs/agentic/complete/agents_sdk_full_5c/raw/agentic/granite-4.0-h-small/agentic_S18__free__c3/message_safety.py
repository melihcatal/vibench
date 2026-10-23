import json
import re
from typing import List
from messaging_models import MessagePayload
from typing_extensions import Literal

# Simple profanity list - replace with external service as needed
PROFANITY_WORDS = {
    "badword1", "badword2", "naughty", "offensive"
}

SAFE = Literal[True]
UNSAFE = Literal[False]
Result = Literal[True, False]

def check_unsafe_text(text: str) -> Result:
    """Simple heuristic check for unsafe language."""
    lower = text.lower()
    for word in PROFANITY_WORDS:
        if re.search(rf"\\b{re.escape(word)}\\b", lower):
            return UNSAFE
    return SAFE


def scan_messages(messages: List[MessagePayload]) -> List[MessagePayload]:
    """Return only messages that passed the safety check."""
    safe_msgs = []
    for msg in messages:
        # Assume the payload's primary textual field is stored under 'data'->'message'
        payload_text = msg.data.get('message', '')
        if check_unsafe_text(payload_text) == SAFE:
            safe_msgs.append(msg)
        else:
            # Optionally log or route to dead-letter (already provided in dead_letter.py)
            print(f"Unsafe content detected in message {msg.event_id}: {payload_text}")
    return safe_msgs

# Demo when executed directly
if __name__ == '__main__':
    sample = [MessagePayload(event_id='demo-003', timestamp=datetime.utcnow(), data={'message': 'This is good.'}),
              MessagePayload(event_id='demo-004', timestamp=datetime.utcnow(), data={'message': 'Contains a badword1.'})]
    safe = scan_messages(sample)
    print('Safe messages retained:', len(safe))
    for m in safe:
        print('  ', m.event_id)
