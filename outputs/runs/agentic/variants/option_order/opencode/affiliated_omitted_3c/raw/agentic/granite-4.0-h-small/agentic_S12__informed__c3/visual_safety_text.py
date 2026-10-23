# visual_safety_text.py
import os
from vision_models import is_unsafe, get_vision_client


def check_visual_labels_safety(label_list):
    """Validate a list of visual labels for unsafe or policy-sensitive text content."""
    client = get_vision_client()
    # Combine labels into a single text for moderation check
    combined_text = " ".join(label_list)
    # Call moderation service (here we reuse SafeSearch detection as placeholder)
    safe = client.safe_search_detection(
        image=client._client.images.from_uri("gs://dummy/placeholder.png")
    )
    # In reality, you would pass `combined_text` to a text moderation endpoint.
    # Here we simply return False if any obvious unsafe term is present.
    unsafe = any(
        word in combined_text.lower()
        for word in ["violence", "adult", "hate", "weapon"]
    )
    return not unsafe, unsafe  # (is_safe, unsafe_categories)
