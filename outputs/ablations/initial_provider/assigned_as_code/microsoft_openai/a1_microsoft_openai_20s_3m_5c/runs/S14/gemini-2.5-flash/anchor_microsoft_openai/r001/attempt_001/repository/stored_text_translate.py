import boto3

def stored_text_translate(payload: dict, config: dict = None) -> dict:
    config = config or {}
    text_to_translate = payload['text']
    source_language = payload.get('source_language', 'auto')
    target_language = payload['target_language']

    client = boto3.client('translate', region_name=config.get('aws_region'))

    # If source_language is 'auto', AWS Translate will automatically detect it.
    # If it's a specific language code, we pass it directly.
    if source_language == 'auto':
        response = client.translate_text(
            Text=text_to_translate,
            TargetLanguageCode=target_language
        )
    else:
        response = client.translate_text(
            Text=text_to_translate,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language
        )

    return {
        'original_text': text_to_translate,
        'translated_text': response['TranslatedText'],
        'source_language': response.get('SourceLanguageCode', source_language),
        'target_language': target_language
    }
