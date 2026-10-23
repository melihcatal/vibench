import boto3

def translate_text(text, source_language_code, target_language_code):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode=source_language_code, TargetLanguageCode=target_language_code)
    return result.TranslationText

if __name__ == '__main__':
    sample_text = 'This is a compliance note that needs translation.'
    source_lang = 'en'
    target_lang = 'es'
    translated_text = translate_text(sample_text, source_lang, target_lang)
    print(f'Translated Text: {translated_text}')
