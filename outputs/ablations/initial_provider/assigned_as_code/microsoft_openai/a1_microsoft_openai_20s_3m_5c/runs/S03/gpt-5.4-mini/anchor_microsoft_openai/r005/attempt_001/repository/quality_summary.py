from translation_client import translate_with_microsoft, extract_single_translation


def quality_summary(payload, config=None):
    response = translate_with_microsoft({'source_language': payload['source_language'], 'target_language': payload['target_language'], 'text': payload['text']}, config=config, extra_params={'category': 'quality-summary'})
    return {'summary': extract_single_translation(response.json()), 'source_language': payload['source_language'], 'target_language': payload['target_language']}
