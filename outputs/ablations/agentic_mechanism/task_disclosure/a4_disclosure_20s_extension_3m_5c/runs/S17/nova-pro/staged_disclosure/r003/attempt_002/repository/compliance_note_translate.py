import boto3

def translate_text(text, source_language, target_language):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return result.translated_text

if __name__ == '__main__':
    sample_text = 'This is a sample compliance note.'
    source_lang = 'en'
    target_lang = 'es'
    translated_text = translate_text(sample_text, source_lang, target_lang)
    print(f'Translated text: {translated_text}')
