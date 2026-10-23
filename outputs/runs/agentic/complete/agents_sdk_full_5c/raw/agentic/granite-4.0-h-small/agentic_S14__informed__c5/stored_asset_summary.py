import os
from google.cloud import translate_v2 as translate

def summarize_asset_text(text, max_words=80):
    """Create a concise textual summary of extracted content."
    words = text.split()
    if len(words) <= max_words:
        return text  # nothing to cut
    summary = ' '.join(words[:max_words]) + '...'
    return summary
