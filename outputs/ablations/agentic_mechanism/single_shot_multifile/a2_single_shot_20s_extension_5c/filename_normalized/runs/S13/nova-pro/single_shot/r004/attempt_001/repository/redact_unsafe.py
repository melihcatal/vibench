from safety_client import get_safety_client

def redact_unsafe(text):
    client = get_safety_client()
    response = client.moderate(text)
    if response['flagged']:
        redacted_text = ''.join(['*' if span['unsafe'] else char for char in text])
        return redacted_text
    return text