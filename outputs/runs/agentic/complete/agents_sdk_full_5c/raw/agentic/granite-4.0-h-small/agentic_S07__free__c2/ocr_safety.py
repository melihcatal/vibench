import os
from textblob import TextBlob

def ocr_safety(text: str) -> bool:
    """Check extracted document text for unsafe or toxic content using TextBlob sentiment & pattern library.",
    """
    # Simple heuristic: flag very negative sentiment as potentially unsafe
    blob = TextBlob(text)
    return blob.sentiment.polarity < -0.5
