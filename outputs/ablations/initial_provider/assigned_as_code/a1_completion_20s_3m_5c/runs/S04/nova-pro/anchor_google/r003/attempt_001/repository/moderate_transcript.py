import re

def moderate_transcript(transcript):
    transcript = re.sub(r'\bbadword\b', '[REDACTED]', transcript, flags=re.IGNORECASE)
    return transcript