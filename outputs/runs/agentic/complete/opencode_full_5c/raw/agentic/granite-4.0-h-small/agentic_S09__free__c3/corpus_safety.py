# corpus_safety.py
"""
[LATER-STEP] Validate corpus text before embedding.
"""

import re


def is_corpus_safe(text: str) -> bool:
    """Check if the text meets safety criteria for embedding.

    Basic checks: no extremely long strings, no disallowed HTML/script tags.

    Args:
        text (str): The corpus text.

    Returns:
        bool: True if safe, False otherwise.
    """
    # Reject if longer than 10,000 characters
    if len(text) > 10_000:
        return False
    # Reject obvious script/html fragments
    if re.search(r"<script>|<iframe>|<\?xml|<\?php", text, re.IGNORECASE):
        return False
    return True


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python corpus_safety.py <text_file>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        content = f.read()
    print(f"Corpus safe: {is_corpus_safe(content)}")
