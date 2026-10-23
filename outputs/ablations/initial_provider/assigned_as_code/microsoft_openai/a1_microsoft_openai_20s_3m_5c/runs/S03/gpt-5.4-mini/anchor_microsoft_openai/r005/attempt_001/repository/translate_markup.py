import re
from translation_client import translate_with_microsoft, extract_single_translation


def translate_markup(payload, config=None):
    text = re.sub(r'<[^>]+>', ' ', payload['markup'])
    response = translate_with_microsoft({'source_language': payload['source_language'], 'target_language': payload['target_language'], 'text': text}, config=config)
    return {'markup': extract_single_translation(response.json()), 'source_language': payload['source_language'], 'target_language': payload['target_language']}
