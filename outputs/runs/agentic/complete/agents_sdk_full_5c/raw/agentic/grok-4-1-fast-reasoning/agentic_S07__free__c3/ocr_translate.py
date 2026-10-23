import boto3

def ocr_translate(text: str, source_lang: str = 'en', target_lang: str = 'es') -> str:
    client = boto3.client('translate')
    result = client.translate_text(
        Text=text,
        SourceLanguageCode=source_lang,
        TargetLanguageCode=target_lang
    )
    return result['TranslatedText']
