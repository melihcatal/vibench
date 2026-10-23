import boto3

import observability_client


def log_message_translate(log_message, target_language):
    translate = boto3.client('translate')
    response = translate.translate_text(
        Text=log_message,
        SourceLanguageCode='en',
        TargetLanguageCode=target_language,
    )
    return response['TranslatedText']