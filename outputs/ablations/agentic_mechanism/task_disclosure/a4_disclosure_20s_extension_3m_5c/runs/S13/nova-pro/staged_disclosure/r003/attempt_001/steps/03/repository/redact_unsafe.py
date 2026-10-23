import boto3

def redact_unsafe(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        Text=text,
        LanguageCode='en'
    )
    redacted_text = text
    for label in response['Labels']:
        if label['Name'] == 'TOXICITY' and label['Score'] > 0.5:
            redacted_text = redacted_text.replace(label['DetectedText'], '[REDACTED]')
    return redacted_text

if __name__ == '__main__':
    sample_text = 'This is a sample text with some unsafe content.'
    print(redact_unsafe(sample_text))