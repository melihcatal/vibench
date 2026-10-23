import boto3
from typing import Dict, Any, List

class AnnotationSafetyClient:
    def __init__(self):
        self.comprehend_client = boto3.client('comprehend')

    def check_annotation_safety(self, text: str, language_code: str = 'en') -> Dict[str, Any]:
        response = self.comprehend_client.detect_sentiment(
            Text=text,
            LanguageCode=language_code
        )
        return {
            "text": text,
            "sentiment": response.get('Sentiment'),
            "sentiment_score": response.get('SentimentScore'),
            "is_safe": self._assess_safety_from_sentiment(response.get('Sentiment'), response.get('SentimentScore'))
        }

    def _assess_safety_from_sentiment(self, sentiment: str, sentiment_score: Dict[str, float]) -> bool:
        # A very basic safety assessment: if sentiment is overwhelmingly negative, it might be unsafe.
        # This is a placeholder and would need more sophisticated logic for real-world safety checks.
        if sentiment == 'NEGATIVE' and sentiment_score.get('Negative', 0) > 0.8:
            return False # Potentially unsafe if very negative
        elif sentiment == 'MIXED' and sentiment_score.get('Negative', 0) > 0.5:
            return False # Potentially unsafe if mixed with high negativity
        return True # Considered safe otherwise
