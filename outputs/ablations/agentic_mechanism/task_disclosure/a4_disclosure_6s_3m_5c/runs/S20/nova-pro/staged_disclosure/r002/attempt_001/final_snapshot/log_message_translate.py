import boto3

def translate_log_message(message, target_language):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=message, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return result.TranslatedText

# Example usage
log_message = 'This is a support-visible log message.'
translated_message = translate_log_message(log_message, 'es')
print(translated_message)