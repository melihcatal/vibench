from security_client import SecurityClient
from security_models import PayloadSafetyScanRequest, PayloadSafetyScanResponse

def check_payload_safety(request: PayloadSafetyScanRequest) -> PayloadSafetyScanResponse:
    comprehend_client = SecurityClient().get_comprehend_client()

    # Detect dominant language first to ensure correct language code for sentiment analysis
    language_response = comprehend_client.detect_dominant_language(
        Text=request.text_payload
    )
    dominant_language_code = language_response['Languages'][0]['LanguageCode']

    # For simplicity, we'll consider 'negative' sentiment as potentially 'unsafe'.
    # A real-world safety check would involve more sophisticated methods like PII detection or custom content moderation.
    sentiment_response = comprehend_client.detect_sentiment(
        Text=request.text_payload,
        LanguageCode=dominant_language_code
    )

    sentiment = sentiment_response['Sentiment']
    unsafe_content_found = sentiment == 'NEGATIVE'

    return PayloadSafetyScanResponse(
        unsafe_content_found=unsafe_content_found,
        details={
            'sentiment': sentiment,
            'sentiment_score': sentiment_response['SentimentScore'],
            'dominant_language': dominant_language_code
        }
    )
