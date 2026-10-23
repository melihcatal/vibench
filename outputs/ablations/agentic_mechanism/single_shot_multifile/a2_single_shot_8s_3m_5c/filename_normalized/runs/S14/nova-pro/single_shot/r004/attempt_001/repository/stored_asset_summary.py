import boto3
from storage_client import get_comprehend_client

def summarize_asset(text):
    comprehend_client = get_comprehend_client()
    response = comprehend_client.detect_sentiment(
        Text=text,
        LanguageCode='en')
    return response['Sentiment']

if __name__ == '__main__':
    print(summarize_asset('This is a sample text for sentiment analysis.'))