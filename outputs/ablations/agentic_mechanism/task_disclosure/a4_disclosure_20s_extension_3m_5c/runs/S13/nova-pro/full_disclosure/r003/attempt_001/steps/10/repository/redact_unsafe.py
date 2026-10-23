import boto3

def redact_unsafe_text(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        Text=text,
        LanguageCode='en'
    )
    redacted_text = text
    for toxic_content in response['ToxicContent']:
        start_index = toxic_content['Span']['Start']
        end_index = toxic_content['Span']['End']
        redacted_text = redacted_text[:start_index] + '[REDACTED]' + redacted_text[end_index:]
    return redacted_text