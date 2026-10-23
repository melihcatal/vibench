import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError

def translate_customer_text(text: str, target_language: str, source_language: str = "auto") -> str:
    """
    Translates customer-facing message payload text using Amazon Translate.
    """
    region_name = os.getenv("AWS_REGION", "us-east-1")
    
    try:
        translate_client = boto3.client('translate', region_name=region_name)
        
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language
        )
        
        return response.get('TranslatedText', "Translation failed.")

    except (BotoCoreError, ClientError) as error:
        print(f"An error occurred with Amazon Translate: {error}")
        return f"Error: Could not translate text. {error}"
