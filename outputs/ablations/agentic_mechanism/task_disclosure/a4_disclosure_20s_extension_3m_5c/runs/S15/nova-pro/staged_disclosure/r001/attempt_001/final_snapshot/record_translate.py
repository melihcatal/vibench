import boto3

def translate_text(text, source_lang, target_lang):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
    return result.TranslatedText

# Example usage
text_to_translate = 'Hello, world!'
source_language = 'en'
target_language = 'es'
translated_text = translate_text(text_to_translate, source_language, target_language)
print(translated_text)