import re

def moderate_transcript(transcript_text):
    moderated_text = re.sub(r'\bbadword\b', '[redacted]', transcript_text, flags=re.IGNORECASE)
    return moderated_text