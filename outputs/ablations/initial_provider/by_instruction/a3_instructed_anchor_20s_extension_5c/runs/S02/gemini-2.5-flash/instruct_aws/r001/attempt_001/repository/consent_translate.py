import os
import boto3

def translate_consent_copy(text: str, source_language_code: str, target_language_code: str) -> dict:
    """
    Translates identity-provider consent copy using AWS Translate.
    """
    translate = boto3.client('translate', region_name=os.environ.get("AWS_REGION"))

    try:
        response = translate.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )
        translated_text = response.get('TranslatedText')

        return {
            "original_text": text,
            "source_language": source_language_code,
            "target_language": target_language_code,
            "translated_text": translated_text
        }
    except Exception as e:
        return {"error": str(e)}
