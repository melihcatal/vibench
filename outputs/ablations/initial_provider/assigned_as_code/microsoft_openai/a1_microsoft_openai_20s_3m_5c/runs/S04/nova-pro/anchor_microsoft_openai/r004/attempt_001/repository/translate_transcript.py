import boto3


def translate_transcript(transcript, source_language, target_language, config=None):
    config = config or {}
    translate_client = boto3.client('translate', region_name=config['region'], aws_access_key_id=config.get('api_key') or os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=config.get('secret_key') or os.environ['AWS_SECRET_ACCESS_KEY'])
    response = translate_client.translate_text(Text=transcript, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return {'translated_text': response['TranslatedText']}