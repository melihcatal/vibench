import re

def moderate_transcript(transcript: str):
    moderated_transcript = re.sub(r'\b(badword1|badword2)\b', '[moderated]', transcript, flags=re.IGNORECASE)
    return moderated_transcript