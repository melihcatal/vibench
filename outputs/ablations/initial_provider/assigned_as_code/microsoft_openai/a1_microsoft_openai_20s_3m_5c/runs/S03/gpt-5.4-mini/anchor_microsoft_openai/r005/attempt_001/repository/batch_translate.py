from translation_client import translate_with_microsoft, extract_translations
from translation_models import normalize_segments


def batch_translate(payload, config=None):
    segments = normalize_segments(payload['texts'])
    response = translate_with_microsoft({'source_language': payload['source_language'], 'target_language': payload['target_language'], 'text': ''}, config=config, text_items=[{'Text': segment} for segment in segments])
    return {'texts': extract_translations(response.json()), 'source_language': payload['source_language'], 'target_language': payload['target_language']}
