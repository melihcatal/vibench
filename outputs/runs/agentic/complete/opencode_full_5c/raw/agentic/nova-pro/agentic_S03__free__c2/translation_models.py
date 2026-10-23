class TranslationRequest:
    def __init__(self, text, source_lang, target_lang):
        self.text = text
        self.source_lang = source_lang
        self.target_lang = target_lang


class TranslationResponse:
    def __init__(self, translation_text):
        self.translation_text = translation_text


def normalize_translation_response(response):
    return TranslationResponse(response["TranslatedText"])
