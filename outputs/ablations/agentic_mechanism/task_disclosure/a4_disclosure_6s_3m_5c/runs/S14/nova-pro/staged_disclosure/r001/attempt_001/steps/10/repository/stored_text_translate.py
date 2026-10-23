import boto3

def translate_text(text, source_language, target_language):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return result.TranslatedText

# Example usage:
# text = 'Hello, world!'
# source_language = 'en'
# target_language = 'es'
# translated_text = translate_text(text, source_language, target_language)
# print(translated_text)