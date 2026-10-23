import boto3

def summarize_asset(bucket_name, object_key):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(
        Text=object_key,
        LanguageCode='en'
    )
    return response['Sentiment']