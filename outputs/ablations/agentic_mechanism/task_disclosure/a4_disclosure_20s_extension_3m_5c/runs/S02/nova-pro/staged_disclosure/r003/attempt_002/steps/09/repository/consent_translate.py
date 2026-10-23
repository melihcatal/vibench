import boto3

def translate_consent_copy(text):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode='es')
    return result.translatedText

if __name__ == '__main__':
    consent_copy = 'This is the identity-provider consent copy to be translated.'
    translated_copy = translate_consent_copy(consent_copy)
    print(translated_copy)