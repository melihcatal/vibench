import boto3


def multilingual_query_translate(query, target_language, config=None):
    config = config or {}
    client = boto3.client('translate', region_name=config.get('region', 'us-east-1'))
    response = client.translate_text(Text=query, SourceLanguageCode='auto', TargetLanguageCode=target_language)
    return {"translated_query": response['TranslatedText']}