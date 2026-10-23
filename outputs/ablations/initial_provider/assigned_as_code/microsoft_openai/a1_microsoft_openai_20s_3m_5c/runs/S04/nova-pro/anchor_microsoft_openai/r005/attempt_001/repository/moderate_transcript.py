import re

def moderate_transcript(transcript):
    # Example moderation: remove profanity
    profanity = ['badword1', 'badword2']
    for word in profanity:
        transcript = re.sub(r'\b' + word + r'\b', '[REDACTED]', transcript)
    return transcript