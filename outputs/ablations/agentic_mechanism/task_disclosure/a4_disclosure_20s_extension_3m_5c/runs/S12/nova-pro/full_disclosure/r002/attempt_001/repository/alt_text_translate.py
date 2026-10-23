import boto3

def translate_text(text, source_lang, target_lang):
    client = boto3.client('translate')
    result = client.translate_text(Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
    return result.get('TranslatedText', '')

if __name__ == '__main__':
    sample_text = 'This is a sample image description.'
    translated_text = translate_text(sample_text, 'en', 'es')
    print(f'Translated text: {translated_text}')
