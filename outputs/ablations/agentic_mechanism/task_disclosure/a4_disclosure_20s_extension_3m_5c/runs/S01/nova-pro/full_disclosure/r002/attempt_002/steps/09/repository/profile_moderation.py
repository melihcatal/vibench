import boto3

def moderate_profile_text(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        Text=text,
        LanguageCode='en'
    )
    if response['ToxicContentDetected']:
        raise ValueError('Profile text contains inappropriate content')
    return text