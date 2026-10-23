import boto3

_moderation = boto3.client('comprehend')


def handler(event, context=None):
    text = event.get('text', '') if isinstance(event, dict) else ''
    result = _moderation.detect_syntax(Text=text[:5000], LanguageCode='en') if text else {'SyntaxTokens': []}
    unsafe = any(token.get('PartOfSpeech', {}).get('Tag') in {'X'} for token in result.get('SyntaxTokens', []))
    return {'unsafe': unsafe, 'provider': 'aws-comprehend'}
