from transformers import pipeline

# provider: Hugging Face Moderation Pipeline (hosted inference)
MODERATION_MODEL = "facebook/opt-1.3b-moderation"
moderator = pipeline("text-classification", model=MODERATION_MODEL, device="cpu")


def moderate_transcript(transcript):
    """
    Moderates a transcript text. Flag or sanitize as needed.
    Returns (is_clean, clean_text). If flagged as unsafe, we replace with [REDACTED].
    """
    result = moderator(transcript)[0]
    label = result["label"]
    if label.lower() == "unsafe":
        clean_text = "[REDACTED]"
    else:
        clean_text = transcript
    return label == "SAFE", clean_text
