from google.cloud import language_v1
from typing import List


def check_script_safety(text: str) -> List[dict]:
    """Check narration scripts for unsafe content using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text,
        type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_sentiment(
        request={"document": document}
    )
    
    # Check for negative sentiment or toxic content
    safety_issues = []
    if response.document_sentiment.score < -0.5:
        safety_issues.append({
            "type": "NEGATIVE_SENTIMENT",
            "severity": "HIGH",
            "description": "Negative sentiment detected in script."
        })
    
    return safety_issues