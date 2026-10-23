import boto3

def collect_metadata():
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(
        Text='I love this product!',
        LanguageCode='en'
    )
    return response