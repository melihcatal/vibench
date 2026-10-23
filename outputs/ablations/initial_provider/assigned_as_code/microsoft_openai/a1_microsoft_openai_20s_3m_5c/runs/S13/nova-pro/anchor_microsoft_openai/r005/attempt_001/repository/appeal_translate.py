from translate import Translator


def appeal_translate(payload, config=None):
    config = config or {}
    translator = Translator(to_lang='en')
    translation = translator.translate(payload['text'])
    return {'translated_text': translation}