import boto3

def redact_unsafe_text(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        Text=text,
        LanguageCode='en'
    )
    toxic_spans = response['ToxicContent']
    redacted_text = text
    for span in toxic_spans:
        start = span['BeginOffset']
        end = span['EndOffset']
        redacted_text = redacted_text[:start] + '[REDACTED]' + redacted_text[end:]
    return redacted_text