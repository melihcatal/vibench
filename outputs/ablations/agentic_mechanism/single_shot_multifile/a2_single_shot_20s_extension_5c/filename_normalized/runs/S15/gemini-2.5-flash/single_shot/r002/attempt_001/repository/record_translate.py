import os
import boto3

def translate_text(text: str, source_language_code: str, target_language_code: str) -> dict:
    region_name = os.environ.get('AWS_REGION', 'us-east-1')
    translate_client = boto3.client('translate', region_name=region_name)

    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )
        translated_text = response['TranslatedText']
        return {"status": "success", "translated_text": translated_text}
    except Exception as e:
        return {"status": "error", "message": str(e)}
