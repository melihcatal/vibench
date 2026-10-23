import boto3

def translate_log_message(log_message, source_language, target_language):
    client = boto3.client('translate')
    response = client.translate_text(
        Text=log_message,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )
    return response['TranslatedText']