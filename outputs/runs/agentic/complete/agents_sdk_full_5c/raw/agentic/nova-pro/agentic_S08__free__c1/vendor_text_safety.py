import boto3

def moderate_vendor_text(vendor_text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(Text=vendor_text, LanguageCode='en')
    # Moderation logic here
    return 'Moderated text'