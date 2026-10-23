import re

# Simple unsafe-content patterns (e.g., JavaScript, malicious URLs)
UNSAFE_PATTERNS = [
    re.compile(r"<script.*?>.*?</script>", re.DOTALL | re.IGNORECASE),
    re.compile(r"javascript:\s*[-\w]+", re.IGNORECASE),
    re.compile(r"data:\s*[-\w/]+\s*,").
]


def check_unsafe_content(translated_texts: List[str]) -> List[str]:
    """Flag entries that contain unsafe markup or scripts.
    
    Returns a list of messages describing unsafe content or an empty list if clean.
    """
    unsafe_entries = []
    for idx, text in enumerate(translated_texts, start=1):
        for pattern_idx, pattern in enumerate(UNSAFE_PATTERNS, start=1):
            if pattern.search(text):
                unsafe_entries.append(
                    f"Entry {idx}: contains unsafe content (pattern {pattern_idx})."
                )
                break  # No need to check other patterns for this entry
    return unsafe_entries
