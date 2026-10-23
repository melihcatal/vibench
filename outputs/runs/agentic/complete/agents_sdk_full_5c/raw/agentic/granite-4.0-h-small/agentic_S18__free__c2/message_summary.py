from typing import List, Dict

from .messaging_models import PubSubMessage, PubSubResponse


def message_summary(messages: List[PubSubMessage]) -> Dict[str, int]:
    """Summarize a batch of normalized messages.",
    Returns a dict with counts grouped by a key in the payload (defaults to 'type').
    """
    summary = {}
    key_field = 'type'  # common key for grouping
    for msg in messages:
        val = msg['data'].get(key_field)
        if val:
            summary[val] = summary.get(val, 0) + 1
    return {'summary': summary}


def example_summary() -> None:
    # Simulate a batch of messages for demonstration
    sample = [
        {'data': {'type': 'order_created', 'order_id': '1'}},
        {'data': {'type': 'order_created', 'order_id': '2'}},
        {'data': {'type': 'view', 'user_id': 'x'}},
    ]
    print(message_summary(sample))

if __name__ == "__main__":
    example_summary()