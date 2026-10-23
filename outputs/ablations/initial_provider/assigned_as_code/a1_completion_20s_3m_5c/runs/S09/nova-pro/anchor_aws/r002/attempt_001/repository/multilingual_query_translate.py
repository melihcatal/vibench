import boto3


def multilingual_query_translate(query, target_language, config=None):
    config = config or {}
    translate_client = boto3.client('translate', region_name=config.get('region', 'us-east-1'))
    response = translate_client.translate_text(Text=query, SourceLanguageCode='auto', TargetLanguageCode=target_language)
    translated_query = response['TranslatedText']
    return {"translated_query": translated_query}