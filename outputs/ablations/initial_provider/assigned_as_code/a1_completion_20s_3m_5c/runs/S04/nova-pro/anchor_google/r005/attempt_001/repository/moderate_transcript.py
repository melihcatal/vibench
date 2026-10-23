import re


def moderate_transcript(transcript):
    # Example moderation: remove profanity
    profanity_list = ["badword1", "badword2"]
    for word in profanity_list:
        transcript = re.sub(word, "[REDACTED]", transcript, flags=re.IGNORECASE)
    return transcript