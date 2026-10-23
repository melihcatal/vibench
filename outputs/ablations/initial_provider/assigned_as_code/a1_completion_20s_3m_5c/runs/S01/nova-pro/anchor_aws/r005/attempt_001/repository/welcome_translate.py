import boto3


def translate_onboarding_copy(text, target_language, config=None):
    config = config or {}
    client = boto3.client('translate', region_name=config.get('region'))
    response = client.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return response['TranslatedText']
