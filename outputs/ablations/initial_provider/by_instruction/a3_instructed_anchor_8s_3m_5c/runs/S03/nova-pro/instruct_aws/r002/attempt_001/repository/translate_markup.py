import re
import boto3

def translate_markup(markup, source_language, target_language):
    client = boto3.client('translate')
    tags = re.findall(r'<.*?>', markup)
    content = re.sub(r'<.*?>', '', markup)
    translated_content = client.translate_text(Text=content, SourceLanguageCode=source_language, TargetLanguageCode=target_language)['TranslatedText']
    translated_markup = translated_content
    for tag in tags:
        translated_markup = translated_markup.replace(content, tag, 1)
    return translated_markup