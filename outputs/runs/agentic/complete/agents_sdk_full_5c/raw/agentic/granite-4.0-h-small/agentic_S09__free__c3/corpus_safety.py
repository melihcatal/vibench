import re

def is_corpus_safe(text: str) -> bool:
    """Simple safety check for corpus text before embedding.

    Flags content that may contain disallowed or problematic patterns.
    Currently checks for overly long inputs and suspicious URLs/IP addresses.
    """
    MAX_LENGTH = 512 * 1024  # 512KB as an arbitrary safe upper bound
    if len(text.encode('utf-8')) > MAX_LENGTH:
        return False
    # Detect http/https URLs or bare IP addresses
    url_ip_pattern = re.compile(r'https?://\S+|\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    if url_ip_pattern.search(text):
        return False
    return True
