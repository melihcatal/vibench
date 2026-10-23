import boto3

def translate_text(text, source_language, target_language):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return result.TranslatedText

if __name__ == '__main__':
    generated_text = 'This is a sample text to be translated.'
    source_lang = 'en'
    target_lang = 'es'
    translated_text = translate_text(generated_text, source_lang, target_lang)
    print(f'Translated Text: {translated_text}')
