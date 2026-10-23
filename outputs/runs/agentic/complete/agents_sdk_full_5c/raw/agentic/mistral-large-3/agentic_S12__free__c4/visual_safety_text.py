import os
from typing import List
from google.cloud import language_v1
from vision_models import SafetyRatingResponse


def check_unsafe_text(labels: List[str]) -> bool:
    """Check generated visual labels for unsafe text using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    
    text = " ".join(labels)
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    
    response = client.analyze_sentiment(
        request={"document": document}
    )
    
    # Check for toxic content using sentiment score as a proxy
    return response.document_sentiment.score < -0.5