import boto3

def redact_unsafe(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        Text=text,
        LanguageCode='en'
    )
    redacted_text = text
    for entity in response['Entities']:
        if entity['Type'] == 'TOXICITY':
            redacted_text = redacted_text[:entity['BeginOffset']] + '[REDACTED]' + redacted_text[entity['EndOffset']:]
    return redacted_text