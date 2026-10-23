import boto3

def translate_payload(payload, source_lang, target_lang):
    client = boto3.client('translate')
    result = client.translate_text(Text=payload, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
    return result.get('TranslatedText')