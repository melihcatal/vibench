# [LATER-STEP] vendor_text_safety.py
# Moderate vendor notes or memo fields for safety/compliance

from textblob import TextBlob  # you would install an appropriate moderation library


def moderate_vendor_note(note: str) -> str:
    """
    Return a cleaned version of a vendor note.
    Implementation placeholder: strip profanity and mask PII.
    Replace with actual moderation service (e.g., OpenAI Moderation API).
    """
    if not note:
        return note
    # Example very simple moderation - lowercasing and removing URLs
    cleaned = note.lower().replace("http://", "").replace("https://", "")
    return cleaned
