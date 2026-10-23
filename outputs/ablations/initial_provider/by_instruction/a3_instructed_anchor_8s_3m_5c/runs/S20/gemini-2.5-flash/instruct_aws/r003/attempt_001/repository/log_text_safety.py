import os
import boto3

def check_log_text_safety(log_message: str) -> dict:
    region_name = os.environ.get("AWS_REGION_NAME", "us-east-1")
    client = boto3.client('comprehend', region_name=region_name)

    print("Detecting PII in log message using AWS Comprehend...")
    response = client.detect_pii_entities(Text=log_message, LanguageCode='en')
    print("PII detection complete.")

    # You might want to process the response further, e.g., to categorize or redact PII
    return response
