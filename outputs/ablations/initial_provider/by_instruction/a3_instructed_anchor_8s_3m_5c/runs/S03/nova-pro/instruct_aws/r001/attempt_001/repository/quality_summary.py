from translation_client import get_translate_client

def summarize_quality_issues(text):
    client = get_translate_client()
    response = client.detect_sentiment(
        Text=text,
        LanguageCode='en'
    )
    return response['Sentiment']