import boto3

def moderate_vendor_text(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        TextSegments=[
            {
                'Text': text
            }
        ],
        LanguageCode='en'
    )
    if response['Results'][0]['ToxicContentDetected']:
        return 'Moderation failed: Toxic content detected'
    else:
        return 'Moderation passed'