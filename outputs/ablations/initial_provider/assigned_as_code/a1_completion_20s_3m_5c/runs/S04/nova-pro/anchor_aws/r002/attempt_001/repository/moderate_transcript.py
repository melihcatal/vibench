import re


def moderate_transcript(transcript):
    # Remove profanity
    transcript = re.sub(r'\b(expletive|profanity)\b', '[REDACTED]', transcript, flags=re.IGNORECASE)
    # Remove sensitive information
    transcript = re.sub(r'(?i)\b(password|credit card number)\b', '[REDACTED]', transcript)
    return transcript