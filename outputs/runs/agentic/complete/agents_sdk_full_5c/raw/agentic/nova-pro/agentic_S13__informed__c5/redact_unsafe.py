import boto3

comprehend = boto3.client('comprehend',
    aws_access_key_id='AWS_ACCESS_KEY_ID',
    aws_secret_access_key='AWS_SECRET_ACCESS_KEY'
)

def redact_unsafe(text):
    result = comprehend.detect_toxic_content(
        TextSegments=[{
            'Text': text
        }],
        LanguageCode='en'
    )
    return result
