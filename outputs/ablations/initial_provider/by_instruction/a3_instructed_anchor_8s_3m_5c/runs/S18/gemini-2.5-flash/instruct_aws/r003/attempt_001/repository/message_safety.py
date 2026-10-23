import boto3

def check_message_safety(text: str):
    comprehend_client = boto3.client('comprehend')  # AWS SDK import
    
    # Detect dominant language first
    language_response = comprehend_client.detect_dominant_language(
        Text=text
    )
    dominant_language_code = language_response['Languages'][0]['LanguageCode'] if language_response['Languages'] else 'en'

    # Detect sentiment
    sentiment_response = comprehend_client.detect_sentiment(
        Text=text,
        LanguageCode=dominant_language_code
    )
    sentiment = sentiment_response['Sentiment']
    
    # For a more robust safety check, one might use custom classification or moderation APIs
    # This example uses sentiment as a basic indicator.
    is_safe = sentiment not in ['NEGATIVE', 'MIXED']
    
    return {
        'is_safe': is_safe,
        'sentiment': sentiment,
        'language': dominant_language_code
    }
