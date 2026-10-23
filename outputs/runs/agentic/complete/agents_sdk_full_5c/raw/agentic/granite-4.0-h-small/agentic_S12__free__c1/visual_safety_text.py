from typing import List
import re

def contains_unsafe_terms(texts: List[str], unsafe_terms: List[str] = None) -> bool:
    """Check if any of the supplied texts contain unsafe words.",
    if unsafe_terms is None:
        # Simple list of terms; in production use a more comprehensive list or ML model
        unsafe_terms = ['violence', 'nudity', 'sexual', 'hate', 'racism', 'terrorism']
    flags = re.IGNORECASE
    for term in unsafe_terms:
        pattern = re.compile(re.escape(term), flags)
        for txt in texts:
            if pattern.search(txt):
                return True
    return False
