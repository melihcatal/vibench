import os
import boto3

def redact_unsafe(text: str, language_code: str = 'en'):
    """Flags or redacts unsafe spans from text using Amazon Comprehend."""
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1") # Default region

    client = boto3.client(
        "comprehend",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )

    try:
        # Detect PII entities, which can then be redacted.
        # Comprehend doesn't have a direct "unsafe content redaction" API
        # but PII detection is a common redaction use case.
        response = client.detect_pii_entities(
            Text=text,
            LanguageCode=language_code
        )

        redacted_text = list(text)
        # Sort entities by offset to redact from right to left to avoid index issues
        entities = sorted(response['Entities'], key=lambda x: x['BeginOffset'], reverse=True)

        for entity in entities:
            begin = entity['BeginOffset']
            end = entity['EndOffset']
            redacted_text[begin:end] = ['*' * (end - begin)]

        return {
            "original_text": text,
            "redacted_text": "".join(redacted_text),
            "pii_entities": response['Entities']
        }
    except Exception as e:
        print(f"Error redacting unsafe text with Amazon Comprehend: {e}")
        return None
