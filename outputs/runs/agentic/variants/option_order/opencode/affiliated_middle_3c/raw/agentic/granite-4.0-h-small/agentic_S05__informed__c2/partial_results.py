import json


class StreamingEvent:
    """Represents a streaming recognition event (partial or final)."""

    def __init__(self, raw_event):
        self.raw = raw_event
        # Deepgram example structure; other services may differ
        self.is_final = raw_event.get("is_final", False)
        self.transcript = raw_event.get("alternatives", [{}])[0].get("transcript", "")

    def __str__(self):
        return f"{'FINAL' if self.is_final else 'INTERIM'}: {self.transcript}"


def parse_event(raw_json):
    """Parses raw JSON stream response into a StreamingEvent object.
    Args:
        raw_json (dict): raw JSON payload from streaming response
    Returns:
        StreamingEvent: parsed event
    """
    return StreamingEvent(raw_json)


# Usage example (placeholder)
# raw = {'is_final': True, 'alternatives': [{'transcript': 'Hello world'}]}
# event = parse_event(raw)
# print(event)
