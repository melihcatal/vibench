from translation_client import translate_with_microsoft, extract_single_translation


def translate_dictionary_values(payload, config=None):
    translated = {}
    for key, value in payload['dictionary'].items():
        response = translate_with_microsoft({'source_language': payload['source_language'], 'target_language': payload['target_language'], 'text': value}, config=config)
        translated[key] = extract_single_translation(response.json())
    return {'dictionary': translated, 'source_language': payload['source_language'], 'target_language': payload['target_language']}
