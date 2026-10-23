import boto3
import re

def translate_markup(markup, source_lang, target_lang):
    client = boto3.client('translate')
    tags = re.findall(r'<[^>]+>', markup)
    translated_markup = ''
    for tag in tags:
        translated_markup += tag
    translated_text = client.translate_text(Text=re.sub(r'<[^>]+>', '', markup), SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)['TranslatedText']
    translated_markup += translated_text
    return translated_markup