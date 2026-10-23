import boto3

# Initialize the Amazon Comprehend client
comprehend = boto3.client('comprehend', region_name='us-east-1')

def detect_toxic_content(text):
    """Detect toxic content in the given text"""
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return True
    else:
        return False