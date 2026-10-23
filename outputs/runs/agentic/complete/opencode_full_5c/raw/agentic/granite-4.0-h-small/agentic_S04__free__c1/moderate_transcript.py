# moderate_transcript.py
import re


def moderate_transcript(transcript_text: str) -> str:
    """Moderate transcript text before publishing.

    For demo purposes, removes profanity and PII. In production, replace
    with a real moderation service (e.g., Perspective API).
    """
    # Simple profanity filter (replace with robust solution)
    profanity_list = ["badword1", "badword2"]
    for bad in profanity_list:
        transcript_text = re.sub(
            rf"\\b{bad}\\b", "[CENSORED]", transcript_text, flags=re.IGNORECASE
        )
    # Mask emails and phone numbers
    transcript_text = re.sub(
        r"\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b",
        "[EMAIL]",
        transcript_text,
    )
    transcript_text = re.sub(
        r"\\b\\d{3}[-.]?\\d{3}[-.]?\\d{4}\\b", "[PHONE]", transcript_text
    )
    return transcript_text
