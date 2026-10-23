import boto3

translate = boto3.client('translate')

def translate_query(text, source_lang, target_lang):
    response = translate.translate_text(Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
    return response.translatedText