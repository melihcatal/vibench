import boto3

# Configuration for Amazon Comprehend
comprehend_region = 'us-west-2'
comprehend_client = boto3.client('comprehend', region_name=comprehend_region)

def detect_toxic_content(text):
    """Detect toxic content in the given text using Amazon Comprehend"""
    response = comprehend_client.detect_sentiment(
        Text=text,
        LanguageCode='en'
    )
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return True
    return False

def detect_pii_entities(text):
    """Detect personally identifiable information (PII) entities in the given text using Amazon Comprehend"""
    response = comprehend_client.detect_pii_entities(
        Text=text,
        LanguageCode='en'
    )
    pii_entities = response['Entities']
    if pii_entities:
        return True
    return False