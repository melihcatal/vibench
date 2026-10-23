from google.cloud import language_v1
from typing import List, Dict


def moderate_transcript(text_content: str) -> Dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    sentiment = client.analyze_sentiment(document=document).document_sentiment

    # You can expand this to include entity analysis, content classification, etc.
    return {
        "score": sentiment.score,
        "magnitude": sentiment.magnitude,
        "overall_sentiment": "positive"
        if sentiment.score > 0
        else ("negative" if sentiment.score < 0 else "neutral"),
    }
