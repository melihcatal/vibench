import boto3

def translate_text(text, source_language, target_language):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return result.TranslatedText

if __name__ == '__main__':
    source_text = 'This is a compliance note that needs translation.'
    source_language = 'en'
    target_language = 'es'
    translated_text = translate_text(source_text, source_language, target_language)
    print(f'Translated Text: {translated_text}')
