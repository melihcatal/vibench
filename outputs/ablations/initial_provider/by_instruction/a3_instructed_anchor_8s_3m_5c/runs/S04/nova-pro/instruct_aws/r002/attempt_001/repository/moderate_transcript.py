import re

def moderate_transcript(transcript_text):
    # Simple profanity filter
    profanity_list = ['badword1', 'badword2']
    for word in profanity_list:
        transcript_text = re.sub(r'\b' + word + r'\b', '[REDACTED]', transcript_text, flags=re.IGNORECASE)
    return transcript_text