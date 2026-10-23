import boto3

def translate_compliance_note(text: str, source_language: str, target_language: str) -> dict:
    translate_client = boto3.client('translate')
    
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )

    return {
        "original_text": text,
        "translated_text": response['TranslatedText'],
        "source_language": source_language,
        "target_language": target_language,
        "provider": "AWS Translate"
    }
