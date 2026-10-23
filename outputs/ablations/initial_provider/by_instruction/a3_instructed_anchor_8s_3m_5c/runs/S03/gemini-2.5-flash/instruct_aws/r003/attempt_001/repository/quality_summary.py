import boto3

def summarize_quality_issues(translated_text: str, target_language_code: str) -> dict:
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(
        Text=translated_text,
        LanguageCode=target_language_code
    )
    return {
        "sentiment": response['Sentiment'],
        "sentiment_score": response['SentimentScore']
    }
