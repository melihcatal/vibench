import boto3

def redact_unsafe(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(Text=text)
    redacted_text = text
    for toxic_span in response['ToxicSpans']:
        redacted_text = redacted_text[:toxic_span['BeginOffset']] + '[REDACTED]' + redacted_text[toxic_span['EndOffset']:]
    return redacted_text