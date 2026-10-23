import boto3

def translate_log_message(log_message, target_language):
    translate = boto3.client('translate')
    response = translate.translate_text(
        Text=log_message,
        SourceLanguageCode='en',
        TargetLanguageCode=target_language
    )
    return response['TranslatedText']

if __name__ == '__main__':
    log_message = 'This is a sample log message.'
    translated_message = translate_log_message(log_message, 'es')
    print(translated_message)