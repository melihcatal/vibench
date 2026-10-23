import os
import boto3

translate = boto3.client('translate')

def translate_text(text, source_language, target_language):
    result = translate.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return result.TranslatedText
