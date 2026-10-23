import boto3

def redact_unsafe(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(Text=text)
    if response['ToxicContentDetected']:
        redacted_text = ''.join(['*' for _ in text])
        return redacted_text
    return text
