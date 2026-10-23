import boto3

def moderate_profile_text(text: str) -> bool:
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        Text=text,
        LanguageCode='en'
    )
    toxic_content_detected = response['ToxicContentDetected']
    return not toxic_content_detected