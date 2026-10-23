import re

def moderate_transcript(transcript):
    moderated_transcript = re.sub(r'\bbadword\b', '[redacted]', transcript, flags=re.IGNORECASE)
    return moderated_transcript