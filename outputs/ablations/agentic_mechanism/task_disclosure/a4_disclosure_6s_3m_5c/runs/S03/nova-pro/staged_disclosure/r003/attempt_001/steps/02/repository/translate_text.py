import boto3

def translate_text(text, source_language, target_language):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return result.get('TranslatedText')

if __name__ == '__main__':
    text_to_translate = 'Hello, world!'
    source_lang = 'en'
    target_lang = 'es'
    translated_text = translate_text(text_to_translate, source_lang, target_lang)
    print(translated_text)