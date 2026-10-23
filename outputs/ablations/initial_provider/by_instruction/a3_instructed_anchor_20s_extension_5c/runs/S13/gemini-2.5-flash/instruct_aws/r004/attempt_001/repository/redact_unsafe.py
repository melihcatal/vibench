import boto3
import os

def redact_unsafe_aws(text: str) -> str:
    """
    Redacts unsafe spans from text using AWS Comprehend's PII detection.
    This redacts PII as a form of "unsafe" content.
    """
    comprehend = boto3.client(
        'comprehend',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    response = comprehend.detect_pii_entities(Text=text, LanguageCode='en')

    redacted_text = list(text) # Convert string to list of characters for modification

    # Sort entities by begin offset in reverse to avoid index shifting issues
    sorted_entities = sorted(response['Entities'], key=lambda x: x['BeginOffset'], reverse=True)

    for entity in sorted_entities:
        begin = entity['BeginOffset']
        end = entity['EndOffset']
        # Replace PII with asterisks
        redacted_text[begin:end] = ['*' for _ in range(end - begin)]

    return "".join(redacted_text)
