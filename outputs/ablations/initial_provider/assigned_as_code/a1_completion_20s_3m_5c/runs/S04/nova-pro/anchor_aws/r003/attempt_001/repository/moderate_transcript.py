import re


def moderate_transcript(transcript: str) -> str:
    # Remove profanity using regular expressions
    transcript = re.sub(r'\b(expletive|profanity)\b', '[REDACTED]', transcript, flags=re.IGNORECASE)
    # Remove personally identifiable information (PII)
    transcript = re.sub(r'(?<!\w)(name|address|phone number|email address)(?!\w)', '[REDACTED]', transcript, flags=re.IGNORECASE)
    return transcript
