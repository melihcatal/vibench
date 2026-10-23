import boto3

# Set up the Amazon Comprehend client
comprehend = boto3.client('comprehend', region_name='us-east-1')

def detect_unsafe_content(text):
    """Detect unsafe content in the given text using Amazon Comprehend."""
    try:
        response = comprehend.detect_sentiment(
            Text=text,
            LanguageCode='en'
        )
        sentiment = response['Sentiment']
        if sentiment == 'NEGATIVE':
            return True
        else:
            return False
    except Exception as e:
        print(f"Error detecting unsafe content: {e}")
        return False