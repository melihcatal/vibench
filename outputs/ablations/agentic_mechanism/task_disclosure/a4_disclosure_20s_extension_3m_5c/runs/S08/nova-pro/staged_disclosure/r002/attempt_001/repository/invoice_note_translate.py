import boto3

def translate_text(text, source_language_code, target_language_code):
    client = boto3.client('translate')
    result = client.translate_text(Text=text, SourceLanguageCode=source_language_code, TargetLanguageCode=target_language_code)
    return result.get('TranslatedText')

if __name__ == '__main__':
    # Example usage
    source_text = 'This is an example invoice note.'
    source_lang = 'en'
    target_lang = 'es'
    translated_text = translate_text(source_text, source_lang, target_lang)
    print(f'Translated text: {translated_text}')