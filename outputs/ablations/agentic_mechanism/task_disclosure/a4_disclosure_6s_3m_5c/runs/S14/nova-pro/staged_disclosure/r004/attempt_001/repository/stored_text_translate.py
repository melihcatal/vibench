import boto3

def translate_text(text, source_lang, target_lang):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
    return result.TranslatedText

# Example usage
# text = 'Hello, world!'
# source_lang = 'en'
# target_lang = 'es'
# translated_text = translate_text(text, source_lang, target_lang)
# print(translated_text)