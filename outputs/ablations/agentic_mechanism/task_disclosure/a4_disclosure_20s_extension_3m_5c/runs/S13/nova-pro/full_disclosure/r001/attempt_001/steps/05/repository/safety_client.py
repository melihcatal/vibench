import boto3

# Configuration for Amazon Comprehend
COMPREHEND_REGION = 'us-west-2'

# Initialize the Amazon Comprehend client
comprehend = boto3.client('comprehend', region_name=COMPREHEND_REGION)

def detect_toxic_content(text):
    """Detect toxic content in the given text using Amazon Comprehend."""
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return True
    return False

def detect_pii_content(text):
    """Detect personally identifiable information (PII) in the given text using Amazon Comprehend."""
    response = comprehend.detect_pii_entities(Text=text, LanguageCode='en')
    pii_entities = response['Entities']
    if pii_entities:
        return True
    return False