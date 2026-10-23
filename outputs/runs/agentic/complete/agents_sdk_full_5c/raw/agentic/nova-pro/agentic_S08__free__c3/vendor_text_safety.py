import boto3

comprehend = boto3.client('comprehend')

def moderate_vendor_text(text):
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    # Moderation logic here
    return moderated_text