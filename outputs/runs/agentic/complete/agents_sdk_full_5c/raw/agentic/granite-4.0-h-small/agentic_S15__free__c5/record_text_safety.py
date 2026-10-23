import re

def contains_unsafe_content(text: str) -> bool:
    """Checks user-generated text for potentially unsafe patterns (e.g., XSS, SQLi).
    Simple regex based check for demonstration purposes.
    
    Args:
        text (str): User-provided text content.
    Returns:
        bool: True if unsafe patterns detected, False otherwise.
    """
    if not text:
        return False
    # Basic patterns - expand as needed
    patterns = [
        re.compile(r"<script.*?>.*?</script>", re.IGNORECASE | re.DOTALL),
        re.compile(r"on\w+\\s*=\\s*['\"]?javascript:.*?['\"]?", re.IGNORECASE),
        re.compile(r"--|/*\\*.*?\\*/"),  # SQL comment hints
    ]
    for pattern in patterns:
        if pattern.search(text):
            return True
    return False


def sanitize_text(text: str) -> str:
    """Attempts to neutralize unsafe characters by escaping HTML tags.
    Returns sanitized string.
    """
    if not text:
        return text
    return re.sub(r"<(/?[^>]+)>", "", text)  # strip HTML tags
