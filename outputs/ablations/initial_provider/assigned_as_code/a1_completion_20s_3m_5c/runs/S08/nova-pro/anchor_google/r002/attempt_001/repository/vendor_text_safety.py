import boto3

def moderate_vendor_text(vendor_text):
    comprehend_client = boto3.client('comprehend')
    response = comprehend_client.detect_sentiment(
        Text=vendor_text,
        LanguageCode='en'
    )
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return 'Moderated text'
    return vendor_text