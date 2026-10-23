import boto3

def moderate_profile_text(profile_text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        Text=profile_text,
        LanguageCode='en'
    )
    if response['ToxicContentDetected']:
        return False
    else:
        return True