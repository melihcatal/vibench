import boto3

# Initialize the Amazon Comprehend client
comprehend = boto3.client('comprehend')

def moderate_claims(text):
    # Detect sentiment to moderate the claims
    sentiment = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    if sentiment['Sentiment'] == 'NEGATIVE':
        return 'Claim may contain negative sentiment.'
    else:
        return 'Claim appears to be neutral or positive.'