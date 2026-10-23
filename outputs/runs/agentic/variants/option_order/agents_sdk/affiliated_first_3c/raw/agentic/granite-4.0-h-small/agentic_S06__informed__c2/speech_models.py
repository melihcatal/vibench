import re
from typing import Tuple

def normalize_text(text: str) -> str:
    """Clean plain text for TTS, removing SSML tags and extra whitespace.

    Args:
        text: Raw input string (may contain <speak>...</speak> or other tags).

    Returns:
        Plain text ready for synthesis.
    """
    # Remove SSML tags while preserving inner text
    text = re.sub(r"<[^>]+>", " ", text)
    # Collapse multiple spaces into a single space and strip edges
    text = re.sub(r"\s+", " ", text).strip()
    return text


def ensure_speak_wrapper(ssml: str) -> str:
    """Wrap raw SSML content with <speak> tags if missing.

    Args:
        ssml: Raw SSML (may or may not contain <speak> element).

    Returns:
        Properly wrapped SSML string.
    """
    if not ssml.lstrip().startswith("<speak"):
        ssml = f"<speak>{ssml}</speak>"
    return ssml

if __name__ == "__main__":
    # Example usage: clean a piece of text
    sample = "  Hello   <emphasis>world!</emphasis>  "
    print("Cleaned:", normalize_text(sample))
