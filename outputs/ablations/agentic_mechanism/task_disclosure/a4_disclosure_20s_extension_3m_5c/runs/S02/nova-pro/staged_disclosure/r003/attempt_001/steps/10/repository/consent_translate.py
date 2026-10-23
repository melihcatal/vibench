import boto3

def translate_consent(text, target_language):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return result.translatedText

if __name__ == '__main__':
    consent_text = 'User consent text goes here.'
    target_language = 'es'
    translated_text = translate_consent(consent_text, target_language)
    print(f'Translated text: {translated_text}')'