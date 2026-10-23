# visual_safety_text.py
# [LATER-STEP] Check generated visual labels for unsafe text

# Placeholder - reuse the safety detection logic from score_image_safety.py
# but apply to textual content extracted from the image.

PROVIDER = "Google Cloud Vision"


def check_text_for_safety(text: str) -> bool:
    """
    Evaluate whether the extracted text contains unsafe words/phrases.
    Returns True if safe, False if unsafe.
    """
    unsafe_words = ["violence", "adult", "sex", "hate", "weapon"]
    # Simple case‑insensitive check
    return not any(word.lower() in text.lower() for word in unsafe_words)
