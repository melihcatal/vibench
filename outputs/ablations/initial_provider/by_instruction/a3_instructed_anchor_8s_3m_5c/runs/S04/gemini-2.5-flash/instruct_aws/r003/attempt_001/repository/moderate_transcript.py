from speech_client import get_comprehend_client
from speech_models import ModerationResult

def moderate_text(text: str, language_code: str = "en") -> ModerationResult:
    comprehend_client = get_comprehend_client()
    try:
        # Using detect_sentiment as an example of moderation, though a real moderation
        # service would likely be Comprehend's content moderation APIs if available,
        # or custom entity recognition for specific terms.
        # For this exercise, we will use detect_dominant_language and detect_sentiment
        # as proxies for demonstrating Comprehend integration.
        
        # Detect dominant language first if not provided, though the prompt assumes it is.
        if not language_code:
            dominant_language_response = comprehend_client.detect_dominant_language(Text=text)
            language_code = dominant_language_response['Languages'][0]['LanguageCode']

        sentiment_response = comprehend_client.detect_sentiment(
            Text=text,
            LanguageCode=language_code
        )

        # In a real scenario, you'd look for specific entities or sentiment scores
        # to determine moderation flags. Here, we'll just return the sentiment.
        moderation_labels = [{
            'Type': 'Sentiment',
            'Score': sentiment_response['SentimentScore'],
            'Sentiment': sentiment_response['Sentiment']
        }]

        print(f"Text moderated with sentiment: {sentiment_response['Sentiment']}")
        return ModerationResult(
            text=text,
            moderation_labels=moderation_labels
        )
    except Exception as e:
        print(f"Error moderating text with AWS Comprehend: {e}")
        raise
