import boto3

def moderate_vendor_text(vendor_text):
    comprehend_client = boto3.client('comprehend')
    response = comprehend_client.detect_toxic_content(
        Text=vendor_text,
        LanguageCode='en'
    )
    return response['Labels']