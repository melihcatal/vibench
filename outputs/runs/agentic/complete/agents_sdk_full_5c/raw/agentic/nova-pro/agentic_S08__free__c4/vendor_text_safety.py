import boto3

comprehend_client = boto3.client('comprehend')

def moderate_vendor_text(vendor_text):
    response = comprehend_client.detect_sentiment(
        Text=vendor_text,
        LanguageCode='en')
    # Moderation logic here
    return is_safe