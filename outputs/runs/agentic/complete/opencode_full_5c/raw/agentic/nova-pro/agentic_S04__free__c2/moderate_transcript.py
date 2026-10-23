import re


def moderate_transcript(transcript_text):
    moderated_text = re.sub(
        r"\b(badword1|badword2)\b", "[moderated]", transcript_text, flags=re.IGNORECASE
    )
    return moderated_text
