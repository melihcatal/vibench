# LATER-STEP
# Verify that generated textual labels contain no unsafe language
import json
from vision_models import normalize_moderation


def check_generated_labels_for_unsafe(labels_path: str, texts_path: str) -> bool:
    """Return True if any unsafe language appears in the text output.

    Reads the moderated flag from the safety check and unsafe words from text extraction.
    """
    # Load moderation result (from score_image_safety)
    moderation = json.load(open(labels_path, "r"))
    unsafe_words = normalize_moderation(moderation)

    # Load extracted text (from detect_image_text)
    extracted_texts = json.load(open(texts_path, "r"))

    # Simple containment check
    for word in unsafe_words:
        for text in extracted_texts:
            if word.lower() in text.lower():
                return False
    return True
