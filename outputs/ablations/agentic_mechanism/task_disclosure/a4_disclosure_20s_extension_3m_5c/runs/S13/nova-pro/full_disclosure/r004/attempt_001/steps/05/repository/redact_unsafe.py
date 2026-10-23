import boto3

def redact_unsafe(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(Text=text)
    redacted_text = text
    for toxic_span in response['ToxicSpans']:
        start = toxic_span['BeginOffset']
        end = toxic_span['EndOffset']
        redacted_text = redacted_text[:start] + '[REDACTED]' + redacted_text[end:]
    return redacted_text