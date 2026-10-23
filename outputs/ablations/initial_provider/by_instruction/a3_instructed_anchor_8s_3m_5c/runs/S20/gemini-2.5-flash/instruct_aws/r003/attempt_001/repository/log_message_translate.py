import os
import boto3

def translate_log_message(log_message: str, target_language_code: str = 'es') -> str:
    region_name = os.environ.get("AWS_REGION_NAME", "us-east-1")
    client = boto3.client('translate', region_name=region_name)

    print(f"Translating log message to {target_language_code} using AWS Translate...")
    response = client.translate_text(
        Text=log_message,
        SourceLanguageCode='en',  # Assuming source language is English
        TargetLanguageCode=target_language_code
    )
    print("Translation complete.")

    return response['TranslatedText']
