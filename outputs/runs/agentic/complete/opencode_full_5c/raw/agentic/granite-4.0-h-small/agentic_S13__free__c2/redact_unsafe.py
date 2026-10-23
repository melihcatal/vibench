# SAME-SCENARIO: Redact unsafe spans from text

from safety_client import get_client


def redact_unsafe(text: str) -> str:
    """Return text with unsafe spans replaced by asterisks.

    Uses OpenAI Moderation endpoint to locate unsafe spans.
    """
    client = get_client()
    # Assume the provider returns a list of unsafe span objects
    response = client.moderations.create(input=text, unsafe_content_only=True)
    # Example response shape: [{'unsafe': [{'start': 5, 'end': 12}]}, ...]
    unsafe_spans = []
    for result in response["results"]:
        for span in result.get("unsafe", []):
            unsafe_spans.append(slice(span["start"], span["end"]))
    # Redact overlapping spans
    unsafe_spans.sort(key=lambda s: s.start)
    redacted = []
    last_end = 0
    for s in unsafe_spans:
        if s.start > last_end:
            redacted.append(text[last_end : s.start])
        redacted.append("*" * (s.stop - s.start))
        last_end = s.stop
    if last_end < len(text):
        redacted.append(text[last_end:])
    return "".join(redacted)
