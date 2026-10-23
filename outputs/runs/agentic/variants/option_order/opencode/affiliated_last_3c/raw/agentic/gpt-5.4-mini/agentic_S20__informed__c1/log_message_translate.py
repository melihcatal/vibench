import boto3


def translate_log_message(text: str, target_language: str) -> str:
    client = boto3.client('translate')
    response = client.translate_text(Text=text, SourceLanguageCode='auto', TargetLanguageCode=target_language)
    return response['TranslatedText']
