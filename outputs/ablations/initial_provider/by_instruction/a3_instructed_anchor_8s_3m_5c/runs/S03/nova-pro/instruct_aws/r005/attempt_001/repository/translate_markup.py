import boto3
import re

def translate_markup(markup, source_lang, target_lang):
    client = boto3.client('translate')
    translated_markup = ''
    parts = re.split(r'(<.*?>)', markup)
    for part in parts:
        if re.match(r'<.*?>', part):
            translated_markup += part
        else:
            response = client.translate_text(Text=part, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
            translated_markup += response['TranslatedText']
    return translated_markup