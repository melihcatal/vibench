import boto3

def moderate_claim(claim_text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        Text=claim_text,
        LanguageCode='en'
    )
    return response
