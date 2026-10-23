import re


def moderate_transcript(transcript):
    # Additional logic to moderate transcript
    moderated_transcript = re.sub(r"\bbadword\b", "moderated", transcript)
    return moderated_transcript
