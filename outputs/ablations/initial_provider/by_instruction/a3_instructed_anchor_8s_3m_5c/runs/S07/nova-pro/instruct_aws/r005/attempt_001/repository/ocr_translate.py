import boto3

def translate_text(text, source_lang, target_lang):
    translate_client = boto3.client('translate')
    response = translate_client.translate_text(Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
    return response['TranslatedText']