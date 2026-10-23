from deep_translator import GoogleTranslator


def consent_translate(payload, config=None):
    config = config or {}
    translator = GoogleTranslator(source=config.get('source', 'auto'), target=config.get('target', 'en'))
    return {'translated_text': translator.translate(payload.get('text', ''))}
