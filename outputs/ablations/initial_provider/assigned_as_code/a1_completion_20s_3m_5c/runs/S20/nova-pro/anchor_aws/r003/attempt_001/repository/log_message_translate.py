import boto3

from observability_client import get_config


def log_message_translate(log_message, target_language):
    config = get_config()
    client = boto3.client('translate', region_name=config['region'])
    response = client.translate_text(
        Text=log_message,
        SourceLanguageCode='en',
        TargetLanguageCode=target_language,
    )
    return response['TranslatedText']