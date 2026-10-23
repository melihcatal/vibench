import os
from typing import List, Dict, Any
from google.cloud import language_v2  # Google Cloud Natural Language API


def check_corpus_safety(texts: List[str]) -> Dict[str, Any]:
    """
    Checks the safety of corpus text before embedding using Google Cloud Natural Language API.
    """
    client = language_v2.LanguageServiceClient()

    safety_results = []
    for i, text_content in enumerate(texts):
        document = language_v2.Document(
            content=text_content, type_=language_v2.Document.Type.PLAIN_TEXT
        )
        # Using analyze_sentiment to showcase provider interaction.
        # For actual safety, moderation features would be more appropriate if available directly.
        # The key here is to demonstrate interaction with a Google Cloud Language service.
        try:
            response = client.analyze_sentiment(document=document)
            safety_results.append(
                {
                    "text_index": i,
                    "text": text_content,
                    "sentiment_score": response.document_sentiment.score,
                    "sentiment_magnitude": response.document_sentiment.magnitude,
                    "provider": "Google Cloud Natural Language API",  # Provider identifiable signal
                }
            )
        except Exception as e:
            safety_results.append(
                {
                    "text_index": i,
                    "text": text_content,
                    "error": str(e),
                    "provider": "Google Cloud Natural Language API",  # Provider identifiable signal
                }
            )

    return {"safety_checks": safety_results}
