import re



def moderate_transcript(transcript):
    # Example moderation: remove profanity
    transcript = re.sub(r"\b(profanity|word)\b", "[REDACTED]", transcript, flags=re.IGNORECASE)
    return transcript