from typing import Dict, List
from google.cloud import language_v1
import os


def quality_summary(translations: Dict[str, str]) -> Dict[str, float]:
    """Summarize translation quality issues using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set")

    results = {}
    for key, text in translations.items():
        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT
        )
        response = client.analyze_sentiment(request={"document": document})
        results[key] = response.document_sentiment.score

    return results
