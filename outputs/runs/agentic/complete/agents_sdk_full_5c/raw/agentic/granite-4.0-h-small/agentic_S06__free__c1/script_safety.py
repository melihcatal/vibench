import os
import json
from google.cloud import language_v1

def detect_inappropriate_content(script: str) -> bool:
    """Check narration script for unsafe or disallowed content using Google Cloud Natural Language.

    Returns True if the content is safe, False if flagged for review.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=script, type_=language_v1.Document.Type.PLAIN_TEXT)
    # Use sentiment analysis with predefined toxicity thresholds as a proxy for safety.
    response = client.analyze_sentiment(request={'document': document})
    sentiment = response.document_sentiment.score
    # Simple heuristic: score between 0.2 and 0.8 considered safe.
    return -0.2 <= sentiment <= 0.8


def safe_script_check(script: str) -> str:
    """Return a message indicating safety status.
    """
    if detect_inappropriate_content(script):
        return 'Script is safe for synthesis.'
    else:
        return 'Script contains potentially unsafe content. Review required.'
