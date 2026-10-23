import boto3

def redact_unsafe(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(Text=text)
    redacted_text = text
    for label in response['Labels']:
        if label['Score'] > 0.5:
            redacted_text = redacted_text.replace(label['Name'], '[REDACTED]')
    return redacted_text
