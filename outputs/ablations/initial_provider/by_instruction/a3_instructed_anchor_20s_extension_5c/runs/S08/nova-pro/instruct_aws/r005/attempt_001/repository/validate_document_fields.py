import boto3

def validate_document_fields(document):
    comprehend_client = boto3.client('comprehend')
    response = comprehend_client.detect_sentiment(
        Text=document['text'],
        LanguageCode='en')
    sentiment = response['Sentiment']
    if sentiment!= 'POSITIVE':
        raise ValueError('Invalid sentiment detected')
    if document['confidence'] < 0.9:
        raise ValueError('Low confidence score')