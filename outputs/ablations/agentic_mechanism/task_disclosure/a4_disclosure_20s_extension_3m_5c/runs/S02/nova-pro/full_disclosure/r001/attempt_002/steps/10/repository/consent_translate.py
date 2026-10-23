import boto3

def translate_consent_copy(text, source_language_code, target_language_code):
    client = boto3.client('translate')
    result = client.translate_text(Text=text, SourceLanguageCode=source_language_code, TargetLanguageCode=target_language_code)
    return result.get('TranslatedText', '')

if __name__ == '__main__':
    sample_text = 'Please accept our terms and conditions.'
    translated_text = translate_consent_copy(sample_text, 'en', 'es')
    print(f'Translated text: {translated_text}')
