from document_client import DocumentClient
from document_models import SafetyRequest, SafetyResponse
import logging

logger = logging.getLogger(__name__)

def check_safety(request: SafetyRequest) -> SafetyResponse:
    client = DocumentClient()
    comprehend_client = client.comprehend_client

    # Detect dominant language to use in subsequent calls
    dominant_language_response = comprehend_client.detect_dominant_language(
        Text=request.text
    )
    dominant_language_code = dominant_language_response['Languages'][0]['LanguageCode']

    # For a basic safety check, we can use sentiment analysis
    sentiment_response = comprehend_client.detect_sentiment(
        Text=request.text,
        LanguageCode=dominant_language_code
    )

    # More advanced safety checks would involve custom entity recognition or content moderation APIs
    # For simplicity, we'll consider "unsafe" if the sentiment is overwhelmingly negative.
    # This is a placeholder and would need a more robust definition of "unsafe content".
    is_safe = True
    moderation_labels = []

    if sentiment_response['Sentiment'] == 'NEGATIVE' and sentiment_response['SentimentScore']['Negative'] > 0.8:
        is_safe = False
        moderation_labels.append({'Type': 'Sentiment', 'Label': 'Strongly Negative'})

    return SafetyResponse(is_safe=is_safe, moderation_labels=moderation_labels, raw_response=sentiment_response)
