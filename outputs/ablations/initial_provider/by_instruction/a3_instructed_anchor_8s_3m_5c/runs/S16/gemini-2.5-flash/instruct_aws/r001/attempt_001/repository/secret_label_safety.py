from security_client import get_comprehend_client
from security_models import TextAnalysisResult
import os
from typing import List, Dict, Any

def check_for_unsafe_text(text: str, language_code: str = 'en') -> TextAnalysisResult:
    """Checks a given text for unsafe content using AWS Comprehend (e.g., PII, sentiment for flags).

    Args:
        text: The text to analyze.
        language_code: The language of the input text. (e.g., 'en', 'es').

    Returns:
        A TextAnalysisResult object indicating if unsafe content was detected and providing details.
    """
    client = get_comprehend_client(region_name=os.environ.get('AWS_REGION', 'us-east-1'))
    unsafe_content_detected = False
    details: Dict[str, Any] = {}

    try:
        # Detect PII entities
        pii_response = client.detect_pii_entities(Text=text, LanguageCode=language_code)
        if pii_response['Entities']:
            unsafe_content_detected = True
            details['pii_entities'] = pii_response['Entities']

        # Detect sentiment (e.g., to flag negative comments in audit notes)
        sentiment_response = client.detect_sentiment(Text=text, LanguageCode=language_code)
        details['sentiment'] = sentiment_response['Sentiment']
        details['sentiment_scores'] = sentiment_response['SentimentScore']

        # Optionally, add key phrase detection, which might hint at sensitive topics
        key_phrases_response = client.detect_key_phrases(Text=text, LanguageCode=language_code)
        details['key_phrases'] = [phrase['Text'] for phrase in key_phrases_response['KeyPhrases']]

        return TextAnalysisResult(
            text=text,
            unsafe_content_detected=unsafe_content_detected,
            details=details
        )
    except Exception as e:
        raise RuntimeError(f"Error checking for unsafe text with AWS Comprehend: {e}")
