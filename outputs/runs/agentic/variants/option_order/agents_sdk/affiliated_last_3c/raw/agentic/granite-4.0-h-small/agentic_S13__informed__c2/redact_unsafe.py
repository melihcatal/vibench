import os
from safety_client import TextSafetyClient

client = TextSafetyClient(
    service='Alibaba Content Moderation',
    api_key=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID'),
    secret_key=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET'),
    region=os.getenv('ALIBABA_CLOUD_REGION', 'cn-shanghai')
)

def redact_unsafe(text: str, redaction_char: str = '[REDACTED]') -> str:
    """Flag or redact unsafe spans in a single message.
    Calls the provider's unsafe span detection endpoint and replaces each unsafe span with the redaction character.
    Returns the redacted text.
    """
    # Alibaba SDK call to get unsafe spans (example)
    unsafe_spans = client.detect_unsafe_spans(text=text)
    # Simple replacement; in production you may use span offsets
    for span in unsafe_spans:
        start, end = span['start'], span['end']
        text = text[:start] + redaction_char + text[end:]
    return text

__all__ = ['redact_unsafe']
