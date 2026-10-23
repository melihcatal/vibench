import boto3
import os

def translate_query(
    query: str,
    source_language_code: str = "auto",  # "auto" for automatic detection or specific language code
    target_language_code: str = "en" # Default target to English
) -> str:
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    translate_client = boto3.client(
        service_name="translate",
        region_name=aws_region
    )

    # If source_language_code is "auto", AWS Translate will detect it.
    # Otherwise, a specific language code must be provided.
    if source_language_code == "auto":
        response = translate_client.translate_text(
            Text=query,
            TargetLanguageCode=target_language_code
        )
    else:
        response = translate_client.translate_text(
            Text=query,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )
    
    translated_text = response.get('TranslatedText', query)
    
    return translated_text
