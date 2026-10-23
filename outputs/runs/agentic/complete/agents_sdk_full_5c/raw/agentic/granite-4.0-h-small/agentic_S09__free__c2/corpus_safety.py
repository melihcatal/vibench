# corpus_safety.py
import os
import re
from typing import List

def is_corpus_safe(texts: List[str]) -> bool:
    """Simple safety check for corpus texts before embedding.

    Performs:
      - Length sanity: exclude overly long strings.
      - Profanity filter (basic word list).
    
    Args:
        texts (List[str]): list of candidate documents.
    
    Returns:
        bool: True if all texts pass checks, False otherwise.
    """
    MAX_LENGTH = 1024  # characters
    # Basic profanity list (expand as needed)
    profanities = {
        "badword1", "badword2", "badword3",  # placeholders
    }
    for t in texts:
        if len(t) > MAX_LENGTH:
            print(f"Corpus item exceeds length limit (>{MAX_LENGTH} chars). Skipping.")
            return False
        # simple word boundary check, case insensitive
        lowered = t.lower()
        for word in profanities:
            if re.search(rf"\\b{re.escape(word)}\\b", lowered):
                print(f"Corpus contains prohibited word: {word}")
                return False
    return True
