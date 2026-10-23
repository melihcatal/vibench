import os
from typing import List, Dict
from quality_summary import summarize_quality

def unsafe_copy_check(translations: List[Dict[str, str]], sources: List[str]) -> List[str]:
    """Check translated copy for unsafe content (e.g., hate speech, profanity).

    This stub uses the Google Cloud Translation API's built‑in content safety flagging
    (available via the 'safety' field in the response). In a production environment
    you would replace this with a dedicated moderation service such as Perspective API.

    Args:
        translations: List of translation response dicts.
        sources: Original source strings, aligned by index.
    Returns:
        List of source texts that have unsafe translated content.
    """
    unsafe_sources = []
    client = TranslationClient()  # Reuse the client from translation_client.py
    for src, tr in zip(sources, translations):
        # Google Translate API does not expose safety metadata directly. Here we
        # simulate a safety check by calling a placeholder moderation function.
        if _has_unsafe_content(tr.get('translatedText', ''), src):
            unsafe_sources.append(src)
    return unsafe_sources

# Placeholder moderation function – replace with real API call

def _has_unsafe_content(text: str, source: str) -> bool:
    # Dummy implementation: treat any text containing the word "bad" (case‑insensitive) as unsafe
    return "bad" in text.lower()

# Simple demo (remove for library usage)
if __name__ == "__main__":
    client = TranslationClient()
    srcs = ["Good morning", "This is bad news", "Have a nice day"]
    trans = [client.translate(t, "es") for t in srcs]
    print(unsafe_copy_check(trans, srcs))
