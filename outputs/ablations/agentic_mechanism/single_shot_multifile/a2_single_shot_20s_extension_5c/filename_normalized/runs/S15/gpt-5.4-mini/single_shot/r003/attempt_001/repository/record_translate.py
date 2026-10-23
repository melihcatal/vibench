import boto3

_translate = boto3.client('translate')


def handler(event, context=None):
    text = event.get('text', '') if isinstance(event, dict) else ''
    target = event.get('target_language', 'en') if isinstance(event, dict) else 'en'
    if not text:
        return {'translated_text': '', 'target_language': target}
    response = _translate.translate_text(Text=text, SourceLanguageCode='auto', TargetLanguageCode=target)
    return {'translated_text': response.get('TranslatedText', ''), 'target_language': target}
