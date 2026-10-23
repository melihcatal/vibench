import boto3

def moderate_claims(claims):
    comprehend = boto3.client('comprehend')
    toxic_content = []
    for claim in claims:
        response = comprehend.detect_toxic_content(Text=claim, LanguageCode='en')
        if response['ToxicContent']:
            toxic_content.append(claim)
    return toxic_content