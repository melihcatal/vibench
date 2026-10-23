import os
from typing import Dict, List
from google.cloud import language_v1
from translation_models import TranslationRequest

def quality_summary(
    source_text: str,
    translated_text: str,
    source_lang: str,
    target_lang: str,
) -> Dict[str, float]:
    """Summarize translation quality issues using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    
    source_document = language_v1.Document(
        content=source_text, type_=language_v1.Document.Type.PLAIN_TEXT, language=source_lang
    )
    target_document = language_v1.Document(
        content=translated_text, type_=language_v1.Document.Type.PLAIN_TEXT, language=target_lang
    )
    
    source_analysis = client.analyze_sentiment(request={"document": source_document})
    target_analysis = client.analyze_sentiment(request={"document": target_document})
    
    sentiment_diff = abs(
        source_analysis.document_sentiment.score - target_analysis.document_sentiment.score
    )
    magnitude_diff = abs(
        source_analysis.document_sentiment.magnitude - target_analysis.document_sentiment.magnitude
    )
    
    return {
        "sentiment_deviation": sentiment_diff,
        "magnitude_deviation": magnitude_diff,
        "quality_score": max(0.0, 1.0 - sentiment_diff - magnitude_diff * 0.1),
    }