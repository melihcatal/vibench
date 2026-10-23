import boto3

def translate_text(text, source_lang, target_lang):
    client = boto3.client('translate')
    result = client.translate_text(Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
    return result['TranslatedText']