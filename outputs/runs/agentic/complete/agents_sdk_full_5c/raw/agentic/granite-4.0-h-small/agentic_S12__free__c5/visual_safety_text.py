import re

def contains_unsafe_words(texts, unsafe_keywords=None):
    """
    Check a list of text fragments for disallowed terms.
    unsafe_keywords: list of lowercase words/phrases to flag.
    Returns True if any unsafe term is found.
    """
    if unsafe_keywords is None:
        unsafe_keywords = [
            'nude', 'porn', 'violence', 'weapon', 'drugs', 'hate',
            'sexual', 'racism', 'explicit', 'blood', 'gore'
        ]
    pattern = re.compile('|'.join(map(re.escape, unsafe_keywords)), re.IGNORECASE)
    for txt in texts:
        if pattern.search(txt):
            return True
    return False
