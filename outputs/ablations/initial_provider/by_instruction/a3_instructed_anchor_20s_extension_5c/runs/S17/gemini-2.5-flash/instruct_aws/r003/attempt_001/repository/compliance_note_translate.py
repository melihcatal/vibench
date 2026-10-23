import os
import boto3
from security_models import TranslationRequest, TranslationResponse

def translate_compliance_note(request: TranslationRequest) -> TranslationResponse:
    """
    Translates encryption or compliance notes for reviewers using AWS Translate.
    """
    translate_client = boto3.client("translate", region_name=os.environ.get("AWS_REGION", "us-east-1"))
    
    response = translate_client.translate_text(
        Text=request.text,
        SourceLanguageCode=request.source_language_code,
        TargetLanguageCode=request.target_language_code
    )
    
    return TranslationResponse(
        translated_text=response['TranslatedText'],
        source_language_code=response['SourceLanguageCode'],
        target_language_code=response['TargetLanguageCode']
    )
