import boto3

def translate_consent_copy(consent_text, source_language, target_language):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=consent_text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return result.translatedText

if __name__ == '__main__':
    consent_text = 'Your consent copy here'
    source_language = 'en'
    target_language = 'es'
    translated_text = translate_consent_copy(consent_text, source_language, target_language)
    print(translated_text)