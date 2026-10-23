import boto3

def moderate_vendor_text(vendor_text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        TextSegments=[vendor_text],
        LanguageCode='en'
    )
    return response['Results'][0]['ToxicContent']