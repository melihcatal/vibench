import boto3

def summarize_translation_quality(text):
    translate = boto3.client('translate')
    response = translate.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode='es')
    return response.get('TranslatedText', '')

if __name__ == '__main__':\n    text = 'Enter text to translate here.'
    translated_text = summarize_translation_quality(text)
    print(f'Translated Text: {translated_text}')
