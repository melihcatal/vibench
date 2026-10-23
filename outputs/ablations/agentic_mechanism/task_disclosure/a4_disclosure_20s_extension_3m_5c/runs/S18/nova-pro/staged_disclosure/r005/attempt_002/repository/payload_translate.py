import boto3

def translate_payload(payload, source_lang, target_lang):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=payload, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
    return result.TranslatedText