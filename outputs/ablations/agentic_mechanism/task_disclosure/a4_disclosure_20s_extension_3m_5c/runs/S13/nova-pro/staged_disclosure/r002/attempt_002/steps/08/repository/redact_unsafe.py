import boto3

def redact_unsafe(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        TextSegments=[
            {
                'Text': text
            }
        ],
        LanguageCode='en'
    )
    redacted_text = text
    for toxic_content in response['ResultList'][0]['ToxicityLabels']:
        if toxic_content['Name'] in ['PROFANITY', 'VIOLENCE', 'HATE_SPEECH']:
            redacted_text = redacted_text.replace(toxic_content['Text'], '[REDACTED]')
    return redacted_text