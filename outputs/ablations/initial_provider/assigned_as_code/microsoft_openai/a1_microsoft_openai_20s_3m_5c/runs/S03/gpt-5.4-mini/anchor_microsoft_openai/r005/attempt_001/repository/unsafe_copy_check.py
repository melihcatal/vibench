from translation_client import translate_with_microsoft


def unsafe_copy_check(payload, config=None):
    response = translate_with_microsoft({'source_language': payload['source_language'], 'target_language': payload['target_language'], 'text': payload['text']}, config=config, extra_params={'category': 'unsafe-copy-check'})
    return {'flagged': 'unsafe' in response.text.lower(), 'source_language': payload['source_language'], 'target_language': payload['target_language']}
