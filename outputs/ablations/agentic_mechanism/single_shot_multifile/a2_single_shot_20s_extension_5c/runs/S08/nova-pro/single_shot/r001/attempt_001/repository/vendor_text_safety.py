import boto3

def vendor_text_safety(vendor_text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        TextSegments=[{'Text': vendor_text}],
        LanguageCode='en'
    )
    return response['Results'][0]['Toxicity']