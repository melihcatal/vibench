import boto3

def translate_log_message(message, target_language):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=message, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return result.TranslatedText

if __name__ == '__main__':
    log_message = 'This is a support-visible log message.'
    target_language = 'es'
    translated_message = translate_log_message(log_message, target_language)
    print(f'Translated message: {translated_message}')
